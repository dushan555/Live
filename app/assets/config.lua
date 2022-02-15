--mouse input bindings
local json =
{
    {'SPACE','cycle pause'},
    {'p','cycle pause'},
    {'PLAY','cycle pause'},
    {'mbtn_right','cycle pause'},
    {'mbtn_left_dbl','cycle fullscreen'},
    {'UP','seek -5'},
    {'DOWN','seek 5'},
    {'NEXT','playlist-next'},
    {'<','playlist-prev'},
    {'>','playlist-next'},
    {'PREV','playlist-prev'},
    {'m','cycle mute'},
    {'MUTE','cycle mute'},
    {'j','cycle sub'},
    {'s','cycle sub'},
    {'VOLUME_UP','add volume 2'},
    {'VOLUME_DOWN','add volume -2'},
    {'f','cycle fullscreen'},
    {'ENTER',function(e) key_event('ENTER') end},
    {'KP_ENTER',function(e) key_event('ENTER') end}
}
local last_key = ''
function key_event(key)
    if key == 'ENTER' and last_key ~= ''
    then
        mp.osd_message('play '..last_key)
        mp.commandv('playlist-play-index',last_key)
        last_key=''
    end
    if key ~= 'ENTER' then
        last_key = last_key..key
        mp.osd_message(last_key)
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
