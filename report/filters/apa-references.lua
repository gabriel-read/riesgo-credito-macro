-- Presentation only: retain the admitted BibTeX types and complete source metadata.
function Pandoc(doc)
  local references = pandoc.utils.references(doc)
  for _, reference in ipairs(references) do
    if reference.title then
      -- Keep literal compound-word hyphens together; leave BibTeX/DOIs intact.
      reference.title = pandoc.utils.stringify(reference.title):gsub('%-', '\u{2011}')
    end
    if pandoc.utils.stringify(reference.id) == 'fred2026' then
      reference.type = 'dataset'
    end
    local authors = reference.author or {}
    if #authors == 1 and authors[1].literal and reference.publisher then
      local author = pandoc.utils.stringify(authors[1].literal)
      local publisher = pandoc.utils.stringify(reference.publisher)
      if author == publisher then
        reference.publisher = nil
      end
    end
  end
  doc.meta.references = references
  doc.meta.bibliography = nil
  -- Materialize citation links before the following presentation filter.
  -- Keep Quarto's later citation pass from appending a second bibliography.
  doc = pandoc.utils.citeproc(doc)
  doc.meta['suppress-bibliography'] = true
  return doc
end
