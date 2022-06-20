--mouse input bindings
local json =
{
    {'q','quit'},
    {'SPACE','cycle pause'},
    {'p','cycle pause'},
    {'PLAY','cycle pause'},
    {'mbtn_right','cycle pause'},
    {'mbtn_left_dbl','cycle fullscreen'},
    {'UP','playlist-prev'},
    {'DOWN','playlist-next'},
    {'LEFT','seek -5'},
    {'RIGHT','seek 5'},
    {'NEXT','playlist-next'},
    {'PREV','playlist-prev'},
    {'<','playlist-prev'},
    {'>','playlist-next'},
    {'m','cycle mute'},
    {'MUTE','cycle mute'},
    {'j','cycle sub'},
    {'s','cycle sub'},
    {'VOLUME_UP','add volume 2'},
    {'VOLUME_DOWN','add volume -2'},
    {'+','add volume 2'},
    {'-','add volume -2'},
    {'f','cycle fullscreen'},
    {'ENTER',function(e) key_event('ENTER') end},
    {'KP_ENTER',function(e) key_event('ENTER') end},
    {'BS',function(e) key_event('CLEAR') end},
    {'DEL',function(e) key_event('CLEAR') end},
    {'KP_DEC',function(e) key_event('CLEAR') end}
}

local last_key = ''
local curr_key = ''
function key_event(key)
    if key == 'ENTER' and last_key ~= '' and last_key ~= curr_key
    then
        mp.osd_message('play '..last_key)
        mp.commandv('playlist-play-index',last_key)
        curr_key=last_key
        last_key=''
    end
    if key ~= 'ENTER' then
        if key == 'CLEAR' then
            last_key=''
            mp.osd_message('CLEAR')
        else
            last_key = last_key..key
            mp.osd_message(last_key)
        end
    end
end

for i=0,9 do
    local index_tb = {i}
    table.insert(index_tb,function(e) key_event(i) end)
    table.insert(json,index_tb)
    local kp_index_tb = {'KP'..i}
    table.insert(kp_index_tb,function(e) key_event(i) end)
    table.insert(json,kp_index_tb)
end
mp.set_key_bindings(json, 'input', 'force')

mp.enable_key_bindings('input')
mp.set_property('referrer', 'mgtv.com baidu.com')
function on_property_change(name, value)
    if type(value) == 'string' then
        mp.osd_message(value)
    end
end
mp.observe_property('media-title','string',on_property_change)
mp.commandv('loadlist','live.m3u8')