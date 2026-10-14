-- Resolve named sources from the single generated registry, in every target format.
local destinations = {}
local combined = false

function Meta(meta)
  combined = meta['annex-links-internal'] == true
  local file = io.open('outputs/informe/destinos.json', 'r') or io.open('../outputs/informe/destinos.json', 'r')
  if not file then error('Missing generated source destinations') end
  destinations = pandoc.json.decode(file:read('*a'))
  file:close()
end

function Strong(element)
  local slug = pandoc.utils.stringify(element)
  if not slug:match('^A[TF]%-[A-Z0-9%-]+$') then return nil end
  local row = destinations[slug]
  if not row then error('Unknown source slug: ' .. slug) end
  local file = FORMAT == 'docx' and 'anexo-tecnico.docx' or 'anexo-tecnico.pdf'
  local fragment = FORMAT == 'docx' and '#' or '#nameddest='
  local target = combined and ('#' .. row.anchor) or (file .. fragment .. row.anchor)
  if not combined and FORMAT ~= 'docx' and row.page then
    target = target .. '&page=' .. string.format('%d', row.page)
  end
  return pandoc.Link(pandoc.Str('Anexo ' .. row.annex .. ', ' .. slug), target)
end

function Link(element)
  if FORMAT == 'typst' and element.target:match('^https?://') and pandoc.utils.stringify(element.content) == element.target then
    -- An explicit label avoids Typst's implicit URL hyphen insertion; keep ASCII
    -- display text and the original DOI/URL destination unchanged.
    if element.target:match('^https://doi%.org/') then
      local label = pandoc.write(pandoc.Pandoc({pandoc.Plain(element.content)}), 'typst'):gsub('%s+$', '')
      element.content = {pandoc.RawInline('typst', '#box[' .. label .. ']')}
    else
      element.content = {pandoc.Span(element.content)}
    end
  end
  if FORMAT == 'docx' and not combined then
    element.target = element.target:gsub('^anexo%-tecnico%.pdf#nameddest=', 'anexo-tecnico.docx#')
  elseif not combined then
    local anchor = element.target:match('^anexo%-tecnico%.pdf#nameddest=([a-z0-9%-]+)$')
    local row = anchor and destinations[anchor:upper()]
    if row and row.page then element.target = element.target .. '&page=' .. string.format('%d', row.page) end
  end
  return element
end

function Table(element)
  local text = pandoc.utils.stringify(element)
  if text:find('Criterio cualitativo de alerta', 1, true) then
    return {pandoc.Para({pandoc.Strong({pandoc.Str('Tabla 8')})}),
            pandoc.Para({pandoc.Emph({pandoc.Str('Tablero de alertas tempranas')})}), element}
  end
  return element
end

function Div(element)
  if element.classes:includes('compact-body-table') and FORMAT == 'typst' then
    local text = pandoc.write(pandoc.Pandoc(element.content), 'typst')
    return pandoc.RawBlock('typst', '#block(breakable: false)[' .. text .. ']')
  end
  if not element.classes:includes('literature-summary') then return nil end
  element = element:walk({Table = function(tbl)
    local widths = {0.9, 0.8, 1.45, 1.5, 2.35}
    local specs = tbl.colspecs
    if #specs ~= #widths then error('Literature summary must retain its five columns') end
    for i, width in ipairs(widths) do specs[i][2] = width / 7 end
    tbl.colspecs = specs
    return tbl
  end})
  if FORMAT == 'typst' and #element.content >= 3 then
    -- Keep the label, caption and complete-table link with the first table row.
    local header = pandoc.write(pandoc.Pandoc({element.content[1], element.content[2], element.content[3]}), 'typst')
    local blocks = {pandoc.RawBlock('typst', '#block(sticky: true)[' .. header .. ']')}
    for i = 4, #element.content do blocks[#blocks + 1] = element.content[i] end
    element.content = blocks
  end
  return element
end

function Image(element)
  local name = element.src:match('/(stress_model[12])%.png$')
  if name then
    element.src = '../outputs/informe/' .. name .. '_presentacion.png'
  end
  -- Source information is already present inside each approved figure.
  local caption = pandoc.utils.stringify(element.caption)
  local title = caption:match('^(.-)%. Fuente:')
  if title and not element.src:match('/delinquency_unemployment_ffr%.png$') then element.caption = {pandoc.Str(title)} end
  return element
end

function Figure(element)
  -- Quarto stores the printed caption separately from the image alt text.
  local caption = pandoc.utils.stringify(element.caption.long)
  local title = caption:match('^(.-)%. Fuente:')
  local macro = false
  element:walk({Image = function(img) if img.src:match('/delinquency_unemployment_ffr%.png$') then macro = true end end})
  if macro then return element end
  if title then element.caption.long = {pandoc.Plain({pandoc.Str(title)})} end
  return element
end

return {{Meta = Meta}, {Strong = Strong, Link = Link, Table = Table, Div = Div, Image = Image, Figure = Figure}}
