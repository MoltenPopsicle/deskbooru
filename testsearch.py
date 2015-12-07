from db import db
tags_input = raw_input("Tags to search for (separate by a space):")
tags_search = tags_input.split(' ')
db().search(tags_search)
