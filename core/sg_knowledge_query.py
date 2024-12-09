import streamlit as st

def check_chapter(chapter, knowledge_list):
    chapter_tags = chapter.get('knowledge_tags', [])
    for tag in chapter_tags:
        if tag not in knowledge_list:
            return False
    return True

def knowledge_query(knowledge_list, db):
    suggestions = []
    chapter_index = 1
    flags = [False] * 10
    while True:
        flags[chapter_index] = True
        current_chapter = db.query(f"MATCH (c:Chapter {{id: {chapter_index}}}) RETURN c LIMIT 1")[0]['c']
        if check_chapter(current_chapter, knowledge_list) == False:
            sections = db.query(f"MATCH (c:Chapter {{id: {chapter_index}}})-[:CONTAINS]->(s:Section) RETURN s")
            for section in sections:
                section_tags = section['s'].get('knowledge_tags', [])
                for tag in section_tags:
                    if tag not in knowledge_list:
                        suggestions.append(section['s']['title'])
                        if len(suggestions) >= 3:
                            return suggestions
        next_chapters = db.query(f"MATCH (c1:Chapter {{id: {chapter_index}}})-[:LEARN_NEXT]->(c2:Chapter) RETURN c2")
        for next_chapter in next_chapters:
            next_chapter_index = next_chapter['c2']['id']
            if flags[next_chapter_index] == True:
                continue
            chapter_index = next_chapter_index
            break
    return suggestions
