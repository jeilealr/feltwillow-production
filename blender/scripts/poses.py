"""Small reproducible pose controls. Bone geometry never changes scale."""
import math
from mathutils import Vector


def apply_pose(rig, name):
    if name not in {'neutral','walk','lie','struggle','head_turn'}:
        raise ValueError(name)
    for p in rig.pose.bones:
        p.location=(0,0,0);p.rotation_mode='XYZ';p.rotation_euler=(0,0,0);p.scale=(1,1,1)
    def move_world(bone, delta):
        p=rig.pose.bones[bone]
        p.location=p.bone.matrix_local.to_3x3().inverted() @ Vector(delta)
    if name=='head_turn':
        rig.pose.bones['head'].rotation_euler[1]=math.radians(22)
        rig.pose.bones['neck'].rotation_euler[0]=math.radians(8)
    if name=='walk':
        for tag,amount in [('front_L',.12),('front_R',-.12),('hind_L',-.12),('hind_R',.12)]:
            move_world('CTRL_'+tag,(0,amount,.05 if amount>0 else 0))
        rig.pose.bones['tail_02'].rotation_euler[1]=.15
    if name in {'lie','struggle'}:
        # Rest torso low and extend paws in local forward direction.
        move_world('hips',(0,0,-.34))
        for tag in ['front_L','front_R','hind_L','hind_R']:
            move_world('CTRL_'+tag,(0,-.30 if tag.startswith('front') else .15,0))
        rig.pose.bones['neck'].rotation_euler[0]=-.24
        rig.pose.bones['head'].rotation_euler[1]=.13
    if name=='struggle':
        rig.pose.bones['neck'].rotation_euler[0]=.18
        rig.pose.bones['head'].rotation_euler[1]=-.18
        rig.pose.bones['tail_02'].rotation_euler[0]=.25
    # Render-time eye closure uses existing eyes; neutral restores visibility.
    for o in rig.users_collection[0].objects:
        if o.name.startswith(('Leo_eyelid_','Leo_sclera_','Leo_iris_','Leo_pupil_','Leo_glint_')):
            o.hide_render=name=='lie'
        if o.name.startswith('Leo_sleep_lid_'):
            o.hide_render=name!='lie'
    rig['active_pose']=name
