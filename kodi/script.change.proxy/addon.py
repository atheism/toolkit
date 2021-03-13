import os
import xbmc
import xbmcaddon
import xbmcgui
#import logging
#import addon_utils

addon       = xbmcaddon.Addon()
addonname   = 'HTTP(S) Proxy' #addon.getAddonInfo('name')

# Set a string variable to use
if 'http_proxy' in os.environ:
    result = '***Current http(s)_proxy: ' + os.environ.get('http_proxy')
else:
    result = '!!!No Proxy, Change to set to http://127.0.0.1:51080'

notice = 'Keep to keep current setting unchanged'

#response = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":"script.tubecast","params":{"enabled":false}}')
#result = result + response

#id=xbmcaddon.Addon(id='script.tubecast').getAddonInfo('id')
#result = result + ' ' + id
# Launch a dialog box in kodi showing the string variable 'line1' as the contents
#xbmcgui.Dialog().ok(addonname, result)
toChange = xbmcgui.Dialog().yesno(heading=addonname, message=result, nolabel='Keep', yeslabel='Change')

if toChange:
    if 'http_proxy' in os.environ:
        del os.environ['http_proxy']
        del os.environ['https_proxy']
        del os.environ['no_proxy']
    else:
        os.environ['http_proxy'] = 'http://127.0.0.1:51080'
        os.environ['https_proxy'] = 'http://127.0.0.1:51080'
        os.environ['no_proxy'] = '127.0.0.1,192.168.0.0/16,111.202.0.0/16,121.29.0.0/16,211.204.0.0/16,.cctv.cn,.bilivideo.com,.iqiyi.com'


xbmc.log('Now restart tubecast to reload proxy set', level=xbmc.LOGWARNING)
#xbmc.executebuiltin('StopScript("script.tubecast")')
#xbmc.executebuiltin('EnableAddon("script.tubecast")')
#xbmc.executebuiltin('RunAddon("script.tubecast")')


ADDONID = 'script.tubecast'
#query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params":{"addonid":"%s", "properties": "enabled"}' % ADDONID)
#if '"enabled":true' in query:
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s","enabled":false}}' % ADDONID)

#else:
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":true}}' % ADDONID)

#response = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":"script.tubecast","params":{"enabled":true}}')
#addon_utils.disable("script.tubecast")
#addon_utils.enable("script.tubecast")
xbmc.log('Restart tubecast DONE', level=xbmc.LOGWARNING)

