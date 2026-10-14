-- Adapt the single cover metadata to the native title blocks of each writer.
function Meta(meta)
  if meta['cover-date'] then meta.date = meta['cover-date'] end
  if not meta.author or not meta.affiliation then return meta end
  local name = pandoc.utils.stringify(meta.author)
  local institution = pandoc.utils.stringify(meta.affiliation)
  meta['by-author'] = pandoc.MetaList({pandoc.MetaMap({
    name = pandoc.MetaMap({literal = pandoc.MetaInlines({pandoc.Str(name)})}),
    affiliations = pandoc.MetaList({pandoc.MetaMap({name = pandoc.MetaInlines({pandoc.Str(institution)})})})
  })})
  if FORMAT == 'docx' then
    meta.author = pandoc.MetaList({
      pandoc.MetaInlines({pandoc.Str(name)}),
      pandoc.MetaInlines({pandoc.Str(institution)})
    })
    if meta.subtitle then
      meta.author:insert(pandoc.MetaInlines({pandoc.Str(pandoc.utils.stringify(meta.subtitle))}))
      meta.subtitle = nil
    end
  end
  return meta
end
