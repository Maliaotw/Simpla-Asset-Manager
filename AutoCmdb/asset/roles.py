# 定義用戶群組

admin_perms = ['asset.can_view_asset', 'asset.can_view_category', 'asset.can_view_location',
               'asset.can_view_department', 'asset.can_view_userprofile',
               'host.can_view_host']

it_perms = ['host.can_view_host','asset.can_view_asset']

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
