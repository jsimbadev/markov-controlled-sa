-- Share one section counter across theorems, propositions, lemmas and corollaries.
-- PDF uses the corresponding amsthm counter aliases in tex/pdf-only.tex.
local result_types = {thm = true, prp = true, lem = true, cor = true}

local function result_identifier(identifier)
  return result_types[identifier:match("^(%a+)%-")] == true
end

local function replace_number(element, number)
  local replaced = false
  element = element:walk({
    Str = function(inline)
      if not replaced and inline.text:match("^%d+%.%d+$") then
        inline.text = number
        replaced = true
        return inline
      end
    end
  })
  if not replaced then
    error("Cannot find the native result number to replace with " .. number)
  end
  return element
end

return {
  Pandoc = function(document)
    if not quarto.doc.is_format("html") then
      return document
    end

    -- Collect the complete map first so forward and backward references agree.
    local section, counter = 0, 0
    local numbers = {}
    document:walk({
      traverse = "topdown",
      Header = function(header)
        if header.level == 1 and not header.classes:includes("unnumbered") then
          section = section + 1
          counter = 0
        end
      end,
      Div = function(div)
        if result_identifier(div.identifier) and div.classes:includes("theorem") then
          counter = counter + 1
          numbers[div.identifier] = tostring(section) .. "." .. tostring(counter)
        end
      end
    })

    return document:walk({
      Div = function(div)
        local number = numbers[div.identifier]
        if number then
          -- Restrict the rewrite to the result heading, preserving its title,
          -- mathematics, body and any references to other results.
          div.content[1] = div.content[1]:walk({
            Span = function(span)
              if span.classes:includes("theorem-title") then
                return replace_number(span, number)
              end
            end
          })
          return div
        end
      end,
      Link = function(link)
        local number = numbers[link.target:match("^#(.+)$")]
        if number and link.classes:includes("quarto-xref") then
          return replace_number(link, number)
        end
      end
    })
  end
}
