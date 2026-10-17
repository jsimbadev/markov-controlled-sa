local function assumption_identifier(identifier)
  return identifier:gsub("^asm%-", "cnj-")
end

return {
  {
    Div = function(element)
      element.identifier = assumption_identifier(element.identifier)
      return element
    end,
    Cite = function(element)
      for _, citation in ipairs(element.citations) do
        citation.id = assumption_identifier(citation.id)
      end
      return element
    end,
    Link = function(element)
      element.target = element.target:gsub("^#asm%-", "#cnj-")
      return element
    end
  }
}
