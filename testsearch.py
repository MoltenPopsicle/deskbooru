from db import db, search
tags_input = raw_input("Tags to search for (separate by a space):")
tags_search = tags_input.split(' ')
print(tags_search)
hashhh = search().results(tags_search)
print(hashhh)
