t=vk_session.method('friends.getSuggestions', {'count': 10, 'fields': ['bdate','sex','photo_200_orig',"contacts"]})

t1=vk_session.method('friends.getMutual', {'source_uid': 617202016, "target_uid": 89968313,"order":"random","need_common_count":1})
print(len(t1))
