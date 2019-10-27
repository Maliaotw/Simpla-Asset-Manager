# 定義用戶群組


admin_perms = ['asset.can_view_asset', 'category.can_view_category',
               'department.can_view_department', 'userprofile.can_view_userprofile','location.can_view_location',
               'host.can_view_host']

it_perms = ['host.can_view_host','asset.can_view_asset','location.can_view_location']

other_perms = ['asset.can_view_asset']



perms = {
    'OM': admin_perms,
    'HR': admin_perms,
    'IT': it_perms,
    'other': other_perms

}
#
# p = perms.get('CS') or perms.get('other')
# print(p)
