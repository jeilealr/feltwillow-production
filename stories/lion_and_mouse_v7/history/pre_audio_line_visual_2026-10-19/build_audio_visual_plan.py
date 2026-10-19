"""Executed local one-time migration. Edit audio_visual_plan.json afterwards.

Story-specific semantic directions live here as the migration provenance, not
as a second active authoring source. Refuses to overwrite a migrated plan.
"""
from pathlib import Path
import copy
import json
import sys

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from production.audio_visual_plan import read,write,digest,inventory_audio,wav_facts,apply_event
S=ROOT/'stories/lion_and_mouse_v7'
H=Path(__file__).parent


def b(span,action,shot='medium',mode='single',cast=('Milo',),view='local_world',*,family=None,emotion=None,group=None,transition=None,phases=None,lighting=None):
    return dict(span=span,action=action,shot=shot,mode=mode,cast=list(cast),view=view,family=family,
                emotion=emotion,group=group,transition=transition,phases=phases,lighting=lighting)


# Exact semantic clauses, deliberate shots. No timing is assigned from text length.
D={
'S01-L001':[b(None,'Milo explores left to right through his stream-bank world','establishing','pair',view='explorer_path',phases=[{}, {'actors.Milo.pose':'walking_exploring','actors.Milo.anchor':'stream_route_farther'}])],
'S01-L002':[b('every berry bush','Milo peers into a familiar berry bush at mouse height','close',view='berry_world'),b('every hollow log','Milo explores the mouth of the familiar hollow log','close',view='hollow_log_world'),b('nearly every winding path beneath the trees','Milo follows a winding path beneath towering trunks','medium','pair',view='winding_path_world',phases=[{}, {'actors.Milo.anchor':'winding_path','actors.Milo.pose':'walking'}])],
'S01-L003':[b(None,'A distinct deeper path composition shows Milo venturing farther from home','wide','pair',view='farther_path',phases=[{}, {'actors.Milo.anchor':'far_stream_path'}])],
'S01-L004':[b('tiny seeds beneath the tall grass','Cut from seeds under tall grass to Milo enjoying the familiar seed patch','detail','cut_sequence',view='seed_world'),b('sweet berries beside the stream','Milo enjoys berries beside the recognizable stream','close',view='berries_stream'),b('one particularly delicious acorn that took much longer to enjoy than expected','Milo picks up and savors the acorn; keep the longer enjoyment as readable acting keys, not equal time windows','close','multi_key',view='acorn_world',phases=[{},('pick_acorn',{'props.acorn.owner':'Milo','props.acorn.anchor':'Milo_paws'}),('taste_acorn',{'props.acorn.condition':'tasted'})])],
'S02-L001':[b(None,'Milo looks up as the stream-bank afternoon fades toward sunset','medium','pair',view='sunset_look_up',phases=[{}, {'actors.Milo.gaze':'fading_sky'}])],
'S02-L002':[b(None,'Longer sunset shadows cross the familiar stream-bank ground','environment',cast=(),view='long_shadows')],
'S02-L003':[b(None,'Milo realizes with startled urgency that it is late','portrait',view='milo_realization',emotion='startled_realization',transition='portrait_cut')],
'S02-L004':[b('Still holding the acorn, the mouse stood up.','Milo stands with the same acorn still in his paws','medium','pair',view='acorn_stand',phases=[{}, {'actors.Milo.pose':'standing_holding_acorn'}]),b('Then the little traveler set it carefully beside a stone at the stream.','Milo carefully lowers and releases the acorn beside the fixed flat stone','close','pair',view='stone_acorn_placement',phases=[{},('place_acorn',{'props.acorn.owner':'stone','props.acorn.anchor':'stream_flat_stone'})])],
'S03-L001':[b(None,'Milo pauses at the fork with the distant homeward route visible','establishing',view='homeward_distance')],
'S03-L002':[b(None,'Establish the fork and its two distinct routes without changing their topology','wide',view='two_routes')],
'S03-L003':[b(None,'Emphasize the familiar safe long path curving left around the sunny meadow','wide',view='safe_left_meadow',transition='same_location_cut')],
'S03-L004':[b(None,'Cut to the shorter right-hand shortcut as a separate route emphasis','medium',view='short_right_route',transition='same_location_cut')],
'S03-L005':[b(None,'The shortcut leads through quiet unfamiliar trunks; preserve its right-route identity','wide',view='shortcut_entrance')],
'S03-L006':[b(None,'Milo looks up toward the darkening sky','close','pair',view='decision_sky',group='fork_decision',phases=[{}, {'actors.Milo.gaze':'darkening_sky'}])],
'S03-L007':[b(None,'Milo then looks toward the long safe route','close','pair',view='decision_long_path',group='fork_decision',transition='same_state_camera_cut',phases=[{}, {'actors.Milo.gaze':'safe_left_route'}])],
'S03-L008':[b(None,'Milo then looks toward the shortcut; preserve the established route axis','close','pair',view='decision_shortcut',group='fork_decision',transition='same_state_camera_cut',phases=[{}, {'actors.Milo.gaze':'shortcut_right_route'}])],
'S03-L009':[b(None,'Cut decisively to Milo’s face as he chooses the shortcut','portrait',view='milo_decision',emotion='decisive',transition='portrait_cut')],
'S03-L010':[b(None,'Continue the portrait idea with optimistic confidence; use a fresh editorial cut, not automatic image reuse','portrait',view='milo_decision',emotion='hopeful_confidence',transition='portrait_cut')],
'S04-L001':[b(None,'Milo hurries into the shortcut, following the chosen route','wide','pair',view='shortcut_entry',phases=[{}, {'actors.Milo.pose':'running','actors.Milo.anchor':'shortcut_lane'}])],
'S04-L002':[b(None,'Milo passes the recognizable mossy stone at mouse-world scale','medium','pair',view='mossy_stone_pass',phases=[{}, {'actors.Milo.anchor':'past_mossy_stone'}])],
'S04-L003':[b(None,'Milo ducks under the fallen branch without changing the branch geography','close','pair',view='fallen_branch_pass',phases=[{}, {'actors.Milo.pose':'ducking_run','actors.Milo.anchor':'under_branch'}])],
'S04-L004':[b(None,'Milo rounds the old stump in a distinct action view','medium','pair',view='stump_turn',phases=[{}, {'actors.Milo.anchor':'around_stump','actors.Milo.pose':'running'}])],
'S04-L005':[b(None,'A longer path view shows Milo gathering speed toward home','wide','pair',view='shortcut_speed',phases=[{}, {'actors.Milo.pose':'fast_run','actors.Milo.anchor':'shortcut_exit'}])],
'S05-L001':[b(None,'Reveal Leo asleep beneath the great old tree, with an unhurried establishing composition','establishing',cast=('Leo',),view='sleeping_leo_reveal')],
'S05-L002':[b(None,'Cut closer to the mane resting against the grass; Leo stays asleep','detail',cast=('Leo',),view='sleeping_mane_grass',transition='detail_cut')],
'S05-L003':[b(None,'Cut to Leo’s peacefully closed eyes; the same sleeping state persists','detail',cast=('Leo',),view='sleeping_eyes',transition='detail_cut')],
'S05-L004':[b(None,'Cut to the enormous rounded paw lying across the narrow path as a clear obstacle','detail',cast=('Leo',),view='paw_path_obstacle',transition='detail_cut')],
'S05-L005':[b(None,'Milo rounds the root toward the unseen obstructing paw','close','pair',cast=('Milo','Leo'),view='root_paw_approach',group='great_tree_trip',phases=[{}, {'actors.Milo.anchor':'root_turn_near_paw'}])],
'S05-L006':[b(None,'Hold a brief anticipation view at the root and paw; no invented new action','detail',cast=('Milo','Leo'),view='root_paw_approach',group='great_tree_trip')],
'S05-L007':[b(None,'Milo’s startled reaction reads clearly beside the obstacle','portrait',view='milo_whoa',group='great_tree_trip',emotion='startled',transition='portrait_cut')],
'S05-L008':[b(None,'Milo catches the paw and becomes unbalanced; Leo remains asleep','close','pair',cast=('Milo','Leo'),view='paw_trip_contact',group='great_tree_trip',phases=[{},('trip',{'actors.Milo.support':'unbalanced_paw_contact','actors.Milo.pose':'tripping','actors.Milo.anchor':'leo_obstacle_paw'})])],
'S05-L009':[b(None,'Show support lost, airborne tumble, ground roll, then landing against Leo’s nose as four distinct readable states','action','multi_key',cast=('Milo','Leo'),view='tumble_roll_nose',group='great_tree_trip',phases=[('tumble',{'actors.Milo.support':'airborne','actors.Milo.pose':'support_lost'}),{'actors.Milo.pose':'tumbling'},('roll',{'actors.Milo.support':'ground_rolling','actors.Milo.pose':'rolling'}),('land',{'actors.Milo.support':'ground','actors.Milo.pose':'landed_surprised','actors.Milo.anchor':'leo_nose_contact'})])],
'S05-L010':[b(None,'Leo opens his eyes while Milo remains at the nose-contact landing position','close','pair',cast=('Leo','Milo'),view='leo_eye_opening',phases=[{},('wake',{'actors.Leo.awake':True,'actors.Leo.pose':'lying_awake','actors.Leo.gaze':'Milo'})])],
'S05-L011':[b(None,'Leo’s startled question is a speaker portrait; keep the boundary mouth closed','portrait',cast=('Leo',),view='leo_startled_portrait',emotion='startled',transition='portrait_cut')],
'S06-L001':[b('The lion lifted his head in surprise.','Leo raises his head from the same resting body position','close','pair',cast=('Leo','Milo'),view='head_raise',group='great_tree_block',phases=[{}, {'actors.Leo.pose':'head_raised'}]),b('The mouse scrambled down onto the path.','Milo scrambles from the landing contact to the clear path; review support/contact staging later','close','pair',view='milo_scramble_path',group='great_tree_block',phases=[{}, {'actors.Milo.anchor':'ground_path_beside_leo','actors.Milo.pose':'upright'}])],
'S06-L002':[b(None,'Leo’s paw lifts, descends, and plants beside Milo to block the path without pressing on him','action','multi_key',cast=('Leo','Milo'),view='paw_block',group='great_tree_block',phases=[{}, {'actors.Leo.paw':'descending_beside_Milo'},('block_path',{'actors.Leo.paw':'ground_beside_Milo','props.path_obstacle':'blocking'})])],
'S06-L003':[b(None,'Milo freezes beside the newly planted paw','portrait',view='milo_freeze',emotion='frozen_fear',group='great_tree_block',transition='portrait_cut')],
'S06-L004':[b(None,'A close reaction shows Milo’s former concern about getting home receding; avoid an unnecessary flashback reset','portrait',view='milo_priorities',emotion='worried',transition='portrait_cut')],
'S06-L005':[b(None,'Hold Milo’s small, worried realization in an intimate portrait','portrait',view='milo_priorities',emotion='humbled',transition='portrait_cut')],
'S07-L001':[b(None,'Leo speaks with mild annoyance in a grounded portrait','portrait',cast=('Leo',),view='leo_questioning',emotion='mildly_annoyed',transition='portrait_cut')],
'S07-L002':[b(None,'A second questioning portrait keeps Leo’s eyeline toward Milo','portrait',cast=('Leo',),view='leo_questioning',transition='portrait_cut')],
'S07-L003':[b(None,'Cut to Milo’s apologetic face; the stream is mentioned rather than visually resetting the location','portrait',view='milo_apology',emotion='apologetic',transition='portrait_cut')],
'S07-L004':[b(None,'Milo explains the shortcut with anxious sincerity','portrait',view='milo_apology',emotion='anxious_sincere',transition='portrait_cut')],
'S07-L005':[b(None,'Milo gives a small sincere promise in the same dialogue axis','portrait',view='milo_promise',emotion='sincere',transition='portrait_cut')],
'S08-L001':[b(None,'Leo looks down toward the small mouse','close','pair',cast=('Leo',),view='leo_looks_down',phases=[{}, {'actors.Leo.gaze':'Milo'}])],
'S08-L002':[b(None,'A close Milo reaction makes his trembling readable','portrait',view='milo_trembling',emotion='trembling',transition='portrait_cut')],
'S08-L003':[b(None,'A shared low mouse-world view conveys Leo’s size without depicting hypothetical cruelty','shared',cast=('Leo','Milo'),view='power_without_threat')],
'S08-L004':[b(None,'Leo holds restrained composure; do not enact the hypothetical anger','portrait',cast=('Leo',),view='leo_restraint',emotion='restrained',transition='portrait_cut')],
'S08-L005':[b(None,'A readable shared-scale bridge shows Leo’s physical strength and Milo’s smallness','shared',cast=('Leo','Milo'),view='strength_scale_bridge')],
'S08-L006':[b(None,'Leo considers gentleness; his stillness carries the choice','portrait',cast=('Leo',),view='leo_considers_kindness',emotion='thoughtful',transition='portrait_cut')],
'S08-L007':[b(None,'Leo’s expression softens in one small facial change','portrait','pair',cast=('Leo',),view='leo_softening',phases=[{}, {'actors.Leo.expression':'softened'}],transition='portrait_cut')],
'S08-L008':[b(None,'Leo pauses warmly before speaking','portrait',cast=('Leo',),view='leo_kind_dialogue',transition='portrait_cut')],
'S08-L009':[b(None,'Leo gently jokes about the exciting shortcut','portrait',cast=('Leo',),view='leo_kind_dialogue',emotion='gently_amused',transition='portrait_cut')],
'S08-L010':[b(None,'Leo lifts the blocking paw clear and gives Milo room to leave','shared','pair',cast=('Leo','Milo'),view='paw_release',phases=[{},('clear_path',{'actors.Leo.paw':'clear_of_route','props.path_obstacle':'clear'})])],
'S08-L011':[b(None,'Leo gives gentle advice in a close speaker view','portrait',cast=('Leo',),view='leo_kind_dialogue',emotion='gentle',transition='portrait_cut')],
'S08-L012':[b(None,'Milo reacts to being allowed to leave with startled relief','portrait',view='milo_relief',emotion='surprised_relief',transition='portrait_cut')],
'S08-L013':[b(None,'Leo explains the mistake with calm acceptance','portrait',cast=('Leo',),view='leo_kind_dialogue',transition='portrait_cut')],
'S08-L014':[b(None,'Leo reassures Milo that he meant no harm','portrait',cast=('Leo',),view='leo_kind_dialogue',emotion='reassuring',transition='portrait_cut')],
'S08-L015':[b(None,'Leo’s kindness reads clearly in a warm portrait, not a threatening pose','portrait',cast=('Leo',),view='leo_kind_dialogue',transition='portrait_cut')],
'S08-L016':[b(None,'Milo stares up at Leo with a coherent upward eyeline','portrait',view='milo_relief',emotion='astonished',transition='portrait_cut')],
'S08-L017':[b(None,'Hold Milo’s surprised reaction to the anger he expected; do not introduce a false angry-Leo event','portrait',view='milo_relief',transition='portrait_cut')],
'S08-L018':[b(None,'A shared gentle two-shot reveals kindness in the same world state','shared',cast=('Leo','Milo'),view='kindness_two_shot')],
'S08-L019':[b(None,'Milo thanks Leo with a small grateful expression','portrait',view='milo_thanks',emotion='grateful',transition='portrait_cut')],
'S08-L020':[b(None,'Milo’s sincere portrait holds the promise to remember','portrait',view='milo_thanks',transition='portrait_cut')],
'S08-L021':[b(None,'Milo looks hopeful about passing kindness onward','portrait',view='milo_hope',emotion='hopeful',transition='portrait_cut')],
'S08-L022':[b(None,'Leo responds with quiet encouragement','portrait',cast=('Leo',),view='leo_kind_dialogue',emotion='encouraging',transition='portrait_cut')],
'S08-L023':[b(None,'Leo gently urges Milo onward','portrait',cast=('Leo',),view='leo_kind_dialogue',transition='portrait_cut')],
'S08-L024':[b(None,'Leo gestures toward the darkening canopy while the escape route stays clear','shared','pair',cast=('Leo','Milo'),view='sky_gesture',phases=[{}, {'actors.Leo.gaze':'darkening_sky'}])],
'S09-L001':[b(None,'Milo smiles and takes the homeward shortcut lane','medium','pair',view='homeward_return',family='shortcut',lighting='dusk',phases=[{}, {'actors.Milo.pose':'walking_home','actors.Milo.expression':'relieved'}])],
'S09-L002':[b(None,'A brief held foot-placement detail creates the pause in his departure','detail',view='careful_feet',family='shortcut',lighting='dusk')],
'S09-L003':[b(None,'Milo places a careful step, watching the route this time','close','pair',view='careful_feet',family='shortcut',lighting='dusk',phases=[{}, {'actors.Milo.pose':'careful_walk','actors.Milo.gaze':'ground_route'}])],
'S09-L004':[b(None,'Use an explicit time-change view of daylight at the Great Tree to indicate days passing','environment',cast=(),view='days_pass',family='great_tree',lighting='day',transition='time_change')],
'S09-L005':[b(None,'Milo returns to familiar routines in his stream-bank world','medium','pair',view='familiar_routines',family='stream_bank',lighting='day',phases=[{}, {'actors.Milo.pose':'exploring','actors.Milo.anchor':'familiar_stream_route'}])],
'S09-L006':[b(None,'Leo rests again beneath the same favorite tree in daylight','establishing',cast=('Leo',),view='daytime_rest',family='great_tree',lighting='day',phases=[{'actors.Leo.pose':'resting_awake'}])],
'S09-L007':[b(None,'Hold Leo’s peaceful daytime world, unaware of the next encounter','medium',cast=('Leo',),view='daytime_rest',family='great_tree',lighting='day')],
'S10-L001':[b('something small beneath the leaves caught the lion\'s eye','Leo notices a leaf-covered shape along the distant trap path','medium','pair',cast=('Leo',),view='noticing_trigger',phases=[{}, {'actors.Leo.gaze':'leaf_covered_trigger','actors.Leo.pose':'walking'}]),b('as he walked through a distant part of the forest.','A trigger-and-leaves insert establishes the trap geography without moving its anchors','detail',cast=(),view='hidden_trigger',transition='detail_cut')],
'S10-L002':[b(None,'Leo steps closer while the suspended net remains overhead','medium','pair',cast=('Leo',),view='trigger_approach',group='trap_activation',phases=[{}, {'actors.Leo.anchor':'trigger_approach'}])],
'S10-L003':[b(None,'Show paw approaching the trigger, trigger pressed, then the net falling from its registered overhead anchors','action','multi_key',cast=('Leo',),view='trigger_drop',group='trap_activation',phases=[{},('trigger_press',{'props.trigger.phase':'pressed','actors.Leo.anchor':'trigger_contact'}),('net_drop',{'props.net.phase':'falling'})])],
'S10-L004':[b(None,'The falling net settles over Leo while all four paws remain safely grounded','shared','pair',cast=('Leo',),view='net_settle',group='trap_activation',phases=[{},('net_settle',{'props.net.phase':'settled','actors.Leo.pose':'trapped_grounded'})])],
'S11-L001':[b(None,'Leo gives one careful tug against the intact connected net','medium','pair',cast=('Leo',),view='tug_rope_hold',group='tug_and_hold',phases=[{}, {'actors.Leo.pose':'careful_tug'}])],
'S11-L002':[b(None,'Reuse the tug endpoint deliberately to show that the knotted ropes hold firm','medium',cast=('Leo',),view='tug_rope_hold',group='tug_and_hold',transition='shared_boundary')],
'S11-L003':[b(None,'A close Leo portrait registers disbelief behind the stable net opening','portrait',cast=('Leo',),view='leo_trapped_portrait',emotion='disbelief',transition='portrait_cut')],
'S11-L004':[b(None,'Leo’s frustration reads in his face while the same net remains intact','portrait',cast=('Leo',),view='leo_trapped_portrait',emotion='frustrated',transition='portrait_cut')],
'S11-L005':[b(None,'Leo questions the unbroken rope in a close speaker view','portrait',cast=('Leo',),view='leo_trapped_portrait',transition='portrait_cut')],
'S11-L006':[b(None,'A grounded wider view conveys Leo’s power against the intact net','shared',cast=('Leo',),view='strength_under_net')],
'S11-L007':[b(None,'Leo recognizes that strength alone is not freeing him; rope and net state do not change','portrait',cast=('Leo',),view='leo_realizes_limits',emotion='concerned',transition='portrait_cut')],
'S11-L008':[b(None,'Leo raises his head to call for help; narration is voice-over and does not drive speech mouth animation','close','pair',cast=('Leo',),view='leo_calls',phases=[{}, {'actors.Leo.pose':'head_raised_call','actors.Leo.gaze':'forest_distance'}])],
'S11-L009':[b(None,'Cut into the surrounding forest as the call echoes; the trapped lion and net persist offscreen','environment',cast=(),view='forest_echo')],
'S12-L001':[b(None,'Far away, Milo’s ears lift toward the distant call','close','pair',view='milo_hears',group='milo_recognition',phases=[{}, {'actors.Milo.expression':'alert','actors.Milo.gaze':'distant_call'}])],
'S12-L002':[b(None,'Milo recognizes the voice in a close reaction shot','portrait',view='milo_recognition',group='milo_recognition',emotion='recognition',transition='same_state_camera_cut')],
'S12-L003':[b(None,'Milo names the lion in an urgent portrait, with the speaker-mouth pipeline deferred','portrait',view='milo_recognition',group='milo_recognition',emotion='urgent',transition='portrait_cut')],
'S12-L004':[b(None,'Milo turns and starts running toward the sound','medium','pair',view='run_toward_call',group='rescue_run',phases=[{}, {'actors.Milo.pose':'running_to_help','actors.Milo.anchor':'rescue_route_entry'}])],
'S12-L005':[b(None,'Milo clears the roots with approach, airborne stride, and grounded landing','action','multi_key',view='run_over_roots',group='rescue_run',phases=[{},('jump',{'actors.Milo.support':'airborne','actors.Milo.pose':'root_stride_airborne'}),('land',{'actors.Milo.support':'ground','actors.Milo.anchor':'past_roots','actors.Milo.pose':'running_to_help'})])],
'S12-L006':[b(None,'A new run view follows Milo between substantial bushes','medium','pair',view='run_between_bushes',group='rescue_run',phases=[{}, {'actors.Milo.anchor':'between_bushes'}])],
'S12-L007':[b(None,'Milo ducks beneath low branches along the same rescue route','close','pair',view='run_under_branches',group='rescue_run',phases=[{}, {'actors.Milo.anchor':'under_low_branches','actors.Milo.pose':'ducking_run'}])],
'S12-L008':[b(None,'A forward-moving wider view emphasizes commitment to helping, rather than another shortcut decision','wide','pair',view='run_with_purpose',group='rescue_run',phases=[{}, {'actors.Milo.anchor':'rescue_route_progress','actors.Milo.pose':'running_to_help'}])],
'S12-L009':[b(None,'A close moving reaction makes Milo’s concern readable without cutting to an invented new victim','close',view='run_concern',group='rescue_run',emotion='concerned_determined')],
'S12-L010':[b(None,'Milo continues decisively toward the trap, advancing the composition toward the upcoming arrival','wide','pair',view='run_final_approach',group='rescue_run',phases=[{}, {'actors.Milo.anchor':'near_trap_route','actors.Milo.expression':'determined'}])],
}


def main():
    if (S/'audio_visual_plan.json').exists():raise SystemExit('Already migrated; edit the authored plan directly.')
    original=read(H/'dialogue_coverage.json')['lines']
    line_ids=[l['id'] for l in original]
    actual,problems=inventory_audio(ROOT,'voice/narration/lion_and_mouse_v7/en/r001',set(line_ids))
    if problems:raise ValueError(problems)
    assert set(D)==set(actual),(set(D)-set(actual),set(actual)-set(D))
    old_locations=read(H/'location_library.json')
    locs={'schema':'feltwillow.location-reference.v1','story':'lion_and_mouse_v7',
        'policy':'Masters preserve world identity/geography/style. New camera height, close views, portraits and details may be planned. Exact pixels/crops are optional within an explicitly locked shot, never a family-wide requirement.',
        'families':{},'views':{},'prop_references':old_locations.get('props',[])}
    for old in old_locations['locations']:
        family=old.get('physical_location_id') or 'great_tree'
        locs['families'].setdefault(family,{'id':family,'status':'existing_story_location_family','reference_masters':[],
            'world_rules':['Preserve landmark identities and relative geography; a new view does not create a new physical place.','Camera height/framing/focus may vary; preserve physical character/world scale and felt material language.'],
            'landmarks':[]})
        locs['families'][family]['reference_masters'].append(old['id'])
        locs['families'][family]['landmarks'].append({'master_id':old['id'],'description':old['landmarks']})
        locs['views'][old['id']]={'id':old['id'],'family_id':family,'status':'existing_owner_approved_master',
            'purpose':'Canonical location/world reference; not mandatory repeated scene pixels',
            'source':{'path':old['path'],'sha256':old['sha256']},
            'source_provenance':{'path':old['source_path'],'sha256':old['source_sha256']},
            'approval':old.get('v7_owner_approval'),'lighting':old['time'],
            'preserved_landmarks':old['landmarks'],'camera_intent':'existing approved master composition',
            'used_by_beats':[],'generation_provenance':'existing bytes, untouched by this migration'}
    audio_root='voice/narration/lion_and_mouse_v7/en/r001'
    plan={'schema':'feltwillow.audio-line-visual.v1','story':'lion_and_mouse_v7','audio_revision':'r001',
        'authoring_policy':'Audio line → semantic visual beats → flexible still sequences. Cuts are default; pixel/motion continuity is opt-in. Story state persists across every cut.',
        'audio_source':{'root':audio_root,'timing_summary':audio_root+'/timing.json','timing_summary_sha256':digest(ROOT/audio_root/'timing.json'),
            'authority':'actual WAV bytes for duration; matching JSON for spoken text/speaker/style/provenance; r001 timing.json is the scene summary',
            'inspection':'WAV headers/frame counts, hashes and JSON/summary reconciliation; no playback/word alignment claimed'},
        'audio_scene_order':[f'S{n:02d}' for n in range(1,17)],'audio_scenes':[],
        'script_line_order':line_ids,'lines':[],'initial_world_state':'WORLD_INITIAL',
        'world_states':{},'world_events':{},'state_rules':[], 'continuity_groups':{},
        'migration_provenance':{'history':str(H.relative_to(ROOT)),'legacy_unit_piece_ids':'retained only in the historical snapshot; not used for new beat/image IDs'},
        'planning_review_notes':['Phrase/key timing is pending alignment; no equal subdivisions are authored.',
            'Ground/nose contact for the S05 landing and S06 scramble needs future pose/staging review.',
            'New views need full identity, scale, landmark, support and owner review; a planned view is not an approved master.']}
    def rule(path,edges):
        plan['state_rules'].append({'path':path,'transitions':[{'before':a,'after':b,'event':kind,**({'requires':requires} if requires else {})} for a,b,kind,requires in edges]})
    rule('props.acorn.owner',[('ground','Milo','pick_acorn',[]),('Milo','stone','place_acorn',[])])
    rule('props.acorn.condition',[('whole','tasted','taste_acorn',[])])
    rule('props.path_obstacle',[('sleeping_paw','blocking','block_path',[]),('blocking','clear','clear_path',[])])
    rule('props.trigger.phase',[('unpressed','pressed','trigger_press',[])])
    rule('props.net.phase',[('suspended','falling','net_drop',[{'path':'props.trigger.phase','value':'pressed'}]),('falling','settled','net_settle',[]),('settled','opened','net_open',[{'path':'props.rope.phase','value':'parted'}]),('opened','discarded','net_discard',[{'path':'props.rope.phase','value':'parted'}])])
    rule('props.rope.phase',[('intact','frayed','rope_fray',[]),('frayed','parted','rope_part',[])])
    rule('actors.Leo.awake',[(False,True,'wake',[]),(True,False,'sleep',[])])
    rule('actors.Milo.support',[('ground','unbalanced_paw_contact','trip',[]),('unbalanced_paw_contact','airborne','tumble',[]),('airborne','ground_rolling','roll',[]),('ground_rolling','ground','land',[]),('ground','airborne','jump',[]),('airborne','ground','land',[])])
    world={'actors':{'Milo':{'location_family':'stream_bank','anchor':'near_home_stream_route','pose':'exploring','support':'ground','gaze':'route','expression':'curious','mouth':'closed'},
                     'Leo':{'location_family':'great_tree','anchor':'rest_under_great_tree','pose':'sleeping','support':'ground','gaze':'eyes_closed','expression':'asleep','mouth':'closed','awake':False,'paw':'across_path'}},
        'props':{'acorn':{'owner':'ground','anchor':'stream_acorn_patch','condition':'whole'},'path_obstacle':'sleeping_paw',
                 'trigger':{'phase':'unpressed','location_family':'trap_path'},'net':{'phase':'suspended','location_family':'trap_path','anchor_identity':'trap_ground_anchors_01'},'rope':{'phase':'intact','strand_identity':'main_knot_strand_01'}},
        'world':{'time_of_day':'afternoon','story_period':'first_encounter_day'}}
    current='WORLD_INITIAL';plan['world_states'][current]=copy.deepcopy(world)
    previous=None
    contexts={1:('stream_bank','afternoon'),2:('stream_bank','sunset'),3:('fork','sunset'),4:('shortcut','dusk'),5:('great_tree','dusk'),6:('great_tree','dusk'),7:('great_tree','dusk'),8:('great_tree','dusk'),9:('great_tree','day'),10:('trap_path','morning'),11:('trap_path','morning'),12:('forest_run','morning')}
    def register_view(family,slug,light,shot,bid,action):
        vid=f'{family}__{slug}__{light}'
        if vid not in locs['views']:
            refs=locs['families'][family]['reference_masters']
            locs['views'][vid]={'id':vid,'family_id':family,'status':'planned','purpose':action,
                'reference_masters':refs,'preserved_landmarks':'Use the family landmark register; respect its topology without requiring every landmark visible in a tight shot.',
                'lighting':light,'camera_intent':('Head/ears or full mane, shoulders and upper chest; blurred/shallow-focus family background, valid support may be offscreen.' if shot=='portrait' else f'{shot}: readable subject/action, camera height and framing chosen for this beat, no unexplained anatomical resizing.'),
                'view_realization':'new view or reference-derived framing; method chosen during later image production',
                'used_by_beats':[],'source':None,'generation_provenance':None,'approval':None}
        if bid not in locs['views'][vid]['used_by_beats']:locs['views'][vid]['used_by_beats'].append(bid)
        return vid
    def event(beat,kind,updates):
        nonlocal current,world
        changes=[]
        for path,after in updates.items():
            before=world
            for key in path.split('.'):before=before[key]
            if before!=after:changes.append({'path':path,'before':copy.deepcopy(before),'after':after})
        if not changes:return None
        eid=f"{beat['id']}-E{len([k for k in plan['world_events'] if k.startswith(beat['id']+'-E')])+1:02d}"
        state_id='WORLD_'+eid
        e={'id':eid,'kind':kind,'source_line':beat['line_id'],'changes':changes,'before_state':current,'after_state':state_id}
        world=apply_event(world,e,plan['state_rules']);current=state_id
        plan['world_events'][eid]=e;plan['world_states'][current]=copy.deepcopy(world)
        return eid
    for source in original:
        lid=source['id'];available=lid in actual
        audio=actual[lid] if available else {'status':'not_available_in_r001','revision':'r001','wav':None,'metadata':None,'duration_seconds':None,'sha256':None,'metadata_sha256':None}
        text=audio['metadata_text'] if available else source['text'];speaker=audio['metadata_speaker'] if available else source['speaker']
        line={'line_id':lid,'audio_scene':lid[:3],'speaker':speaker,'text':text,
            'performance_style':audio['metadata_style'] if available else source['performance_direction'],
            'text_source':audio['metadata'] if available else 'SCRIPT.md#'+lid,
            'audio':audio,'planning_status':'planned_pending_owner_review' if available else 'pending_audio_visual_authoring',
            'coverage':{'scope':'complete_line_wav','target_duration_seconds':audio['duration_seconds'],
                'phrase_timing_status':'pending_alignment' if available else 'pending_audio'},'beats':[]}
        for index,spec in enumerate(D.get(lid,[]),1):
            bid=f'{lid}-B{index:02d}';family,light=contexts[source['scene']];family=spec['family'] or family;light=spec['lighting'] or light
            mode=spec['mode'];roles={'single':['single'],'pair':['start','end'],'multi_key':['start','key','end'],'cut_sequence':['single','single']}[mode]
            if spec['phases'] and mode=='multi_key':roles=['start']+['key']*(len(spec['phases'])-2)+['end']
            vid=register_view(family,spec['view'],light,spec['shot'],bid,spec['action'])
            beat={'id':bid,'line_id':lid,'semantic_span':spec['span'] or text,'action':spec['action'],
                'location_family':family,'location_view':vid,'cast':sorted(spec['cast']),
                'offscreen_cast':sorted(set(world['actors'])-set(spec['cast'])),
                'shot_type':spec['shot'],'emotion':spec['emotion'],'camera_intent':locs['views'][vid]['camera_intent'],
                'transition_in':spec['transition'] or ('portrait_cut' if spec['shot']=='portrait' else 'detail_cut' if spec['shot']=='detail' else 'cut'),
                'transition_out':'cut','continuity_group':spec['group'],
                'state_in':current,'entry_events':[],'state_start':None,'state_out':None,
                'timing':{'status':'whole_line' if len(D[lid])==1 else 'pending_alignment','start_seconds':0 if len(D[lid])==1 else None,'end_seconds':audio['duration_seconds'] if len(D[lid])==1 else None},
                'image_sequence':{'mode':mode,'key_timing':'pending_alignment','images':[]},
                'dialogue':{'mode':'narrator_voiceover' if speaker=='NARRATOR' else 'character_dialogue','speaker_character':None if speaker=='NARRATOR' else 'Leo' if speaker=='LION' else 'Milo','mouth_driver':None if speaker=='NARRATOR' else 'future_reviewed_dialogue_pipeline','boundary_mouth':'closed','lip_sync_status':'not_applicable' if speaker=='NARRATOR' else 'pending_recording_alignment_and_reviewed_calibration'},
                'generation_status':'planned_not_generated','review_status':'pending_owner_plan_review'}
            if world['world']['time_of_day']!=light:
                updates={'world.time_of_day':light}
                if lid=='S09-L004':updates['world.story_period']='days_later'
                e=event(beat,'time_change',updates)
                if e:beat['entry_events'].append(e)
                beat['transition_in']='time_change'
            moved={f'actors.{c}.location_family':family for c in spec['cast'] if world['actors'][c]['location_family']!=family}
            if moved:
                e=event(beat,'location_change',moved)
                if e:beat['entry_events'].append(e)
                if beat['transition_in']!='time_change':beat['transition_in']='location_change'
            beat['state_start']=current
            phases=spec['phases'] or [{} for _ in roles]
            if spec['emotion']:
                focal='Leo' if spec['cast']==['Leo'] else 'Milo'
                phases=copy.deepcopy(phases)
                last=phases[-1]
                if isinstance(last,tuple):last[1][f'actors.{focal}.expression']=spec['emotion']
                else:last[f'actors.{focal}.expression']=spec['emotion']
            assert len(phases)==len(roles),(lid,phases,roles)
            for n,(role,update) in enumerate(zip(roles,phases),1):
                kind,updates=update if isinstance(update,tuple) else ('performance',update)
                e=event(beat,kind,updates)
                image_vid=vid
                if mode=='cut_sequence' and n>1:image_vid=register_view(family,spec['view']+'_second_shot',light,'close',bid,spec['action'])
                image={'id':f'{bid}-I{n:02d}','role':role,'status':'planned','location_view':image_vid,
                    'state':current,'events_before':[e] if e else [],'phase_intent':('Action start' if role=='start' else 'Action end' if role=='end' else f'Readable action key {n-1}' if role=='key' else spec['action']),
                    'intra_sequence_transition':'cut' if mode=='cut_sequence' else 'connected_action' if mode in ['pair','multi_key'] else 'hold',
                    'path':None,'sha256':None,'generation_provenance':None,'owner_approval':None}
                if beat['transition_in']=='shared_boundary' and n==1:image['reuse_of']=previous['image_sequence']['images'][-1]['id']
                beat['image_sequence']['images'].append(image)
            beat['state_out']=current
            if beat['continuity_group']:
                plan['continuity_groups'].setdefault(beat['continuity_group'],{'id':beat['continuity_group'],
                    'policy':'Deliberately related action/decision sequence. World state persists; only explicit shared/continuous edges request motion/pixel continuity. Other edges are editorial cuts.', 'beat_ids':[]})['beat_ids'].append(bid)
            if previous:previous['transition_out']=beat['transition_in']
            line['beats'].append(beat);previous=beat
        plan['lines'].append(line)
    root=ROOT/audio_root
    for n in range(1,17):
        ids=[l['id'] for l in original if l['scene']==n];path=root/f'scene{n:02d}.wav'
        plan['audio_scenes'].append({'id':f'S{n:02d}','line_ids':ids,'status':'available_in_r001' if all(lid in actual for lid in ids) else 'not_available_in_r001',
            'assembly':({'path':str(path.relative_to(ROOT)),**wav_facts(path)} if path.is_file() else None)})
    write(S/'audio_visual_plan.json',plan);write(S/'location_library.json',locs)
    write(S/'audio_inventory_r001.json',{'schema':'feltwillow.audio-inventory.v1','audio_root':audio_root,
        'available_lines':actual,'pending_line_ids':[lid for lid in line_ids if lid not in actual],
        'source_files':{'timing.json':digest(root/'timing.json'),'archive_manifest.json':digest(root/'archive_manifest.json'),'SHA256SUMS':digest(root/'SHA256SUMS')},
        'note':'Observed local bytes, not inferred from Git; copied factual inventory, not a second visual authoring source.'})
    print('Authored',len(actual),'available audio lines and retained',len(line_ids)-len(actual),'pending script lines.')

if __name__=='__main__':main()
