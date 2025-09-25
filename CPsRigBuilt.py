import sys
import maya.cmds as mc
from CPsUtils import CPsDisplayImage

from CPsFileStructure import CPsSetupStructure
from CPsControllerDB import CPsLoadFromJson
from CPsControllerJson import ma_file_path

all_constraints = mc.ls(type = 'constraint')
joints = mc.ls(type = 'joint')
suffix = "_ctrl"
group_suffix = "_offset_grp"
joint_group_mapping = {}
mc_file_path = r"D:\clumsypanda\Documents\maya\2024\scripts\automateRig_Tutorial\content\CPsDVControllers\CPsControls.ma"

def CPsBuildRig():
    if mc.window("CPsBuildRigWindow", exists=True):
        mc.deleteUI("CPsBuildRigWindow", window=True)

    mc.window("CPsBuildRigWindow", title="Clumsy Panda Rid Built", widthHeight=(300, 500), s=True)
    # Banner start here
    mc.columnLayout(adjustableColumn=True)
    image_path = CPsDisplayImage('clumsypandastudioBannerRig.png')
    if image_path:
        mc.image(w=300, h=61, image=image_path)
    mc.separator(h=10)
    mc.separator(h=10)
    mc.columnLayout(adjustableColumn=True)
    mc.frameLayout(label=' build', collapsable=True, cl=False)
    mc.rowColumnLayout(nc=1, columnWidth=[(1, 300), (2, 300), (3, 300), (4, 300)])
    mc.button(l="Create Folder Structure", bgc=[0.380, 0.490, 0.020], c=("CPsSetupStructure()"))
    mc.button(l="Delete Edit Marker", bgc=[0.427, 0.463, 0.514], c=("CPsDeleteDressEdit()"))
    mc.button(l="Freeze Joints", bgc=[0.408, 0.502, 0.533], c=("CPsFreezeJointsTransform()"))
    mc.button(l="Make FK Joint", bgc=[0.314, 0, 0], c=("CPsmakeFKJoints()"))
    mc.button(l="importObject", bgc=[0.314, 0, 0], c=("getFile()"))
    mc.button(l="BuildFK", bgc=[0.314, 0, 0], c=("CPsFKSetup()"))
    mc.button(l="BuildSpine", bgc=[0.314, 0, 0], c=("CPsFkrootCtrl()"))
    mc.setParent('..')

    mc.showWindow()

CPsBuildRig()


def CPsDeleteDressEdit():

    #Delete all constraints
    if all_constraints:
        mc.delete(all_constraints)
        print ("All Contraints have been deleted.")

    else:
        print("No contraints found in the scene")

    for joint in joints:
        #make all the joints selectable
        mc.setAttr(f'{joint}.overrideEnabled', 0)
        mc.setAttr(f'{joint}.overrideDisplayType', 0)
    group_name = 'EditMarker'

    if mc.objExists(group_name):
        mc.delete(group_name)
        print (f"Group '{group_name}' and all its children have been deleted.")

    else:
        print(f"Group '{group_name}' does not exist in the scene.")




def CPsFreezeJointsTransform():

    if not joints:
        mc.warning("No joints founts in the scene.")
        return
    for joint in joints:
        #save current transform.
        translate = mc.xform (joint, query= True, translation=True, worldSpace=True)
        rotate = mc.xform(joint, query=True, rotation=True, worldSpace=True)
        scale = mc.xform(joint, query=True, scale=True, worldSpace=True)

        # Freeze transform
        mc.makeIdentity(joint, apply=True, translate=True, rotate=True, scale=True)

        #Reapply saved transform
        mc.xform (joint, translation=translate, worldSpace=True)
        mc.xform(joint, rotation=rotate, worldSpace=True)
        mc.xform(joint, scale=scale, worldSpace=True)



def CPsmakeFKJoints():
    node_to_duplication = "BN_Root"
    new_root_name = "BN_Root1"
    target_group_name = "FK_Setup"
    # Duplication the node and its children
    duplicate_nodes = mc.duplicate(node_to_duplication)
    # Rename the Root joint.
    duplicate_root = duplicate_nodes[0]
    mc.rename(duplicate_root, new_root_name)
    # Check if the target (FK_Setup) group exists
    if mc.objExists(target_group_name):
        # parent the duplication root to the target group
        mc.parent(new_root_name, target_group_name)
    else:
        print(f"Target group '{target_group_name}' does not exist.")
    # parent the name of the duplication nodes
    print("Duplicated nodes:", mc.listRelatives(new_root_name, allDescendents=True) + [new_root_name])
    # Define the prefixes
    old_prefix = "BN_"
    new_prefix = "FK_"
    #Define objects to be deleted
    toeOutL = "FK_FootSideOuter_L"
    toeInL = "FK_FootSideInner_L"
    toeOutR = "FK_FootSideOuter_R"
    toeInR = "FK_FootSideInner_R"
    eyeL = "FK_Eye_L"
    eyeR = "FK_Eye_R"
    headEnd = "FK_HeadEnd"
    jaw = "FK_Jaw"
    thumbL = "FK_ThumbFinger4_L"
    indexL = "FK_IndexFinger4_L"
    middleL = "FK_MiddleFinger4_L"
    ringL = "FK_RingFinger4_L"
    pinkyL = "FK_PinkyFinger4_L"
    thumbR = "FK_ThumbFinger4_R"
    indexR = "FK_IndexFinger4_R"
    middleR = "FK_MiddleFinger4_R"
    ringR = "FK_RingFinger4_R"
    pinkyR = "FK_PinkyFinger4_R"
    toesL = "FK_ToesEnd_L"
    toesR = "FK_ToesEnd_R"
    # Get all the joints under the target group
    fkjoints = mc.listRelatives(target_group_name, allDescendents=True, type='joint', fullPath=True)
    if fkjoints:
        for joint in fkjoints:
            joint_name = joint.split('|')[-1]
            new_name = joint_name
            # check if the joint name start with the old prefix
            if joint_name.startswith(old_prefix):
                # create the new joint name
                new_name = joint_name.replace(old_prefix, new_prefix, 1)
            # check if the joint name is 'FK_Root1
            if new_name == "FK_Root1":
                new_name = "FK_Root"
            full_new_name = '|'.join(joint.split('|')[:-1]) + '|' + new_name
            # check if the new name already exists

            if not mc.objExists(full_new_name):
                try:
                    # Rename the joint
                    mc.rename(joint, new_name)
                except RuntimeError as e:
                    print(f"Error renaming {joint} to {new_name}: {e}")
            else:
                print(f"Name {full_new_name} already exists. Skipping renaming of {joint}.")
        print("Joint Prefixes change Succefully.")
    else:
        print(f"No joint found under the group {target_group_name}.")

    # delete toe In and out
    mc.delete(toeInL,
              toeOutL,
              toeOutR,
              toeInR,
              eyeL,
              eyeR,
              headEnd,
              jaw,
              thumbL,
              indexL,
              middleL,
              ringL,
              pinkyL,
              thumbR,
              indexR,
              middleR,
              ringR,
              pinkyR,
              toesL,
              toesR
              )




def CPsFKSetup():

    def CPsFkHipCtrl():
        def CPsFKHipCtrlL():

            # Define the objects
            hipL = "FK_Hip_L"
            root = "FK_Root"
            setup = "FK_Setup"

            # Unparent "FK_Hip_L" from "FK_Root"
            #mc.parent(hipL, world=True)

            # Reparent "FK_Hip_L" under "FK_Setup"
            mc.parent(hipL, setup)

            # Function to create control structure for a joint
            def create_control_structure(joint_name):
                # Define suffixes
                #suffix = "_ctrl"
                #group_suffix = "_offset_grp"

                # Create two empty groups with specified suffixes
                group1 = mc.group(em=True, name=joint_name + '_grp')
                group2 = mc.group(em=True, name=joint_name + group_suffix)

                # Parent group2 under group1
                mc.parent(group2, group1)

                # Load the control from the JSON file
                try:
                    control_name = CPsLoadFromJson("FK_controller", ma_file_path)
                    print(f"Loaded control: {control_name}")

                    # Check if control_name is a valid object in the scene
                    if not mc.objExists(control_name):
                        raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                    # Parent the control under group2
                    mc.parent(control_name, group2)
                    print(f"Control {control_name} parented under {group2}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                # Define the names
                old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
                new_object_name = joint_name + suffix

                mc.select(old_object_name)
                mc.scale(10, 10, 10, old_object_name)

                mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

                # Rename the object
                if mc.objExists(old_object_name):
                    renamed_object = mc.rename(old_object_name, new_object_name)

                    # Create the group name
                    group_name = joint_name + group_suffix

                    # Check if the group already exists, if not, create it
                    if not mc.objExists(group_name):
                        group_name = mc.group(empty=True, name=group_name)

                    # Parent the renamed object under the group
                    mc.parent(renamed_object, group_name)

                    print(
                        f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
                else:
                    print(f"Object '{old_object_name}' does not exist in the scene.")

                # Match the transformation of group1 to the joint
                mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

                return group1, new_object_name

            # Define the root joint
            root_joint = 'FK_Hip_L'

            # Get all the children of the root joint
            all_children = mc.listRelatives(root_joint, allDescendents=True)

            # Add the root joint to the list of joints to select
            all_joints = [root_joint] + all_children

            # Dictionary to store the top group for each joint
            #joint_group_mapping = {}

            # Iterate through all joints and create control structures
            for joint in all_joints:
                group, control = create_control_structure(joint)
                # Store the top group for each joint
                joint_group_mapping[joint] = group
                # Parent the joint to its corresponding control
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            # Define the specific parent scheme
            parent_scheme = {
                'FK_Knee_L_grp': 'FK_Hip_L',
                'FK_Ankle_L_grp': 'FK_Knee_L',
                'FK_Heel_L_grp': 'FK_Ankle_L',
                'FK_Toes_L_grp': 'FK_Ankle_L',
                'FK_ToesEnd_L_grp': 'FK_Toes_L',
                # 'FK_FootSideOuter_L_grp': 'FK_Toes_L',
                # 'FK_FootSideInner_L_grp': 'FK_Toes_L'
            }

            # Apply the parent scheme
            for child, parent in parent_scheme.items():
                if mc.objExists(child) and mc.objExists(parent):
                    mc.parent(child, parent)
                    print(f"{child} parented to {parent}")
                else:
                    print(f"Skipping {child} -> {parent} as one of them does not exist.")

        CPsFKHipCtrlL()

        def CPsFKHipCtrlR():

            # Define the objects
            hipR = "FK_Hip_R"
            root = "FK_Root"
            setup = "FK_Setup"

            # Unparent "FK_Hip_R" from "FK_Root"
            mc.parent(hipR, setup)

            # Function to create control structure for a joint
            def create_control_structure(joint_name):
                # Define suffixes
                #suffix = "_ctrl"
                #group_suffix = "_offset_grp"

                # Create two empty groups with specified suffixes
                group1 = mc.group(em=True, name=joint_name + '_grp')
                group2 = mc.group(em=True, name=joint_name + group_suffix)

                # Parent group2 under group1
                mc.parent(group2, group1)

                # Load the control from the JSON file
                try:
                    control_name = CPsLoadFromJson("FK_controller", ma_file_path)
                    print(f"Loaded control: {control_name}")

                    # Check if control_name is a valid object in the scene
                    if not mc.objExists(control_name):
                        raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                    # Parent the control under group2
                    mc.parent(control_name, group2)
                    print(f"Control {control_name} parented under {group2}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                # Define the names
                old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
                new_object_name = joint_name + suffix

                mc.select(old_object_name)
                # multiply the scale X 10
                mc.scale(10, 10, 10, old_object_name)
                # Freeze Scale transform
                mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

                # Rename the object
                if mc.objExists(old_object_name):
                    renamed_object = mc.rename(old_object_name, new_object_name)

                    # Create the group name
                    group_name = joint_name + group_suffix

                    # Check if the group already exists, if not, create it
                    if not mc.objExists(group_name):
                        group_name = mc.group(empty=True, name=group_name)

                    # Parent the renamed object under the group
                    mc.parent(renamed_object, group_name)

                    print(
                        f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
                else:
                    print(f"Object '{old_object_name}' does not exist in the scene.")

                # Match the transformation of group1 to the joint
                mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

                return group1, new_object_name

            # Define the root joint
            root_joint = 'FK_Hip_R'

            # Get all the children of the root joint
            all_children = mc.listRelatives(root_joint, allDescendents=True)

            # Add the root joint to the list of joints to select
            all_joints = [root_joint] + all_children

            # Dictionary to store the top group for each joint
            #joint_group_mapping = {}

            # Iterate through all joints and create control structures
            for joint in all_joints:
                group, control = create_control_structure(joint)
                # Store the top group for each joint
                joint_group_mapping[joint] = group
                # Parent the joint to its corresponding control
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            # Define the specific parent scheme
            parent_scheme = {
                'FK_Knee_R_grp': 'FK_Hip_R',
                'FK_Ankle_R_grp': 'FK_Knee_R',
                'FK_Heel_R_grp': 'FK_Ankle_R',
                'FK_Toes_R_grp': 'FK_Ankle_R',
                'FK_ToesEnd_R_grp': 'FK_Toes_R',
                # 'FK_FootSideOuter_R_grp': 'FK_Toes_R',
                # 'FK_FootSideInner_R_grp': 'FK_Toes_R'
            }

            # Apply the parent scheme
            for child, parent in parent_scheme.items():
                if mc.objExists(child) and mc.objExists(parent):
                    mc.parent(child, parent)
                    print(f"{child} parented to {parent}")
                else:
                    print(f"Skipping {child} -> {parent} as one of them does not exist.")

        CPsFKHipCtrlR()

        # Define the names of the groups and joint
        existing_L_group = 'FK_Hip_L_grp'
        existing_R_group = 'FK_Hip_R_grp'
        existing_FK_group = 'FK_Setup'
        main_group_name = 'FKParentToRoot'
        root_joint = 'FK_Root'

        # Check if the existing groups and root joint exist
        l_group_exists = mc.objExists(existing_L_group)
        r_group_exists = mc.objExists(existing_R_group)
        fk_setup_group_exists = mc.objExists(existing_FK_group)
        root_joint_exists = mc.objExists(root_joint)

        if l_group_exists and r_group_exists and root_joint_exists and fk_setup_group_exists:
            # Create the main group
            main_group = mc.group(empty=True, name=main_group_name)

            # Get the transformation matrix of the root joint
            transform_matrix = mc.xform(root_joint, query=True, matrix=True, worldSpace=True)

            # Apply the transformation matrix to the main group
            mc.xform(main_group, matrix=transform_matrix, worldSpace=True)

            # Parent the existing groups under the main group
            mc.parent(existing_L_group, main_group)
            mc.parent(existing_R_group, main_group)
            mc.parent(main_group, existing_FK_group)

            print(f"'{existing_L_group}' and '{existing_R_group}' have been parented under '{main_group}'.")
        else:
            missing_groups = []
            if not l_group_exists:
                missing_groups.append(existing_L_group)
            if not r_group_exists:
                missing_groups.append(existing_R_group)
            if not root_joint_exists:
                missing_groups.append(root_joint)
            print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")


    CPsFkHipCtrl()

    def CPsFKArmCtrl():

        def CPsFKArmCtrlL():

            # Define the objects
            arm = "FK_Scapula_L"
            root = "FK_Chest"
            wrist_joint = 'FK_Wrist_L'
            thumb = "FK_ThumbFinger1_L"
            index = "FK_IndexFinger0_L"
            mid = "FK_MiddleFinger0_L"
            ring = "FK_RingFinger0_L"
            pinky = "FK_PinkyFinger0_L"
            setup = "FK_Setup"
            finger_group_name = 'FKParentToWrist_L'

            l_arm_group_exists = mc.objExists(arm)
            l_thumb_group_exists = mc.objExists(thumb)
            l_index_group_exists = mc.objExists(index)
            l_mid_group_exists = mc.objExists(mid)
            l_ring_group_exists = mc.objExists(ring)
            l_pinky_group_exists = mc.objExists(pinky)

            if l_arm_group_exists and l_thumb_group_exists and l_index_group_exists and l_mid_group_exists and l_ring_group_exists and l_pinky_group_exists:
                # Create the main group
                main_finger_group = mc.group(empty=True, name=finger_group_name)

                # Get the transformation matrix of the root joint
                transform_matrix = mc.xform(wrist_joint, query=True, matrix=True, worldSpace=True)

                # Apply the transformation matrix to the main group
                mc.xform(main_finger_group, matrix=transform_matrix, worldSpace=True)

                # Parent the existing groups under the main group
                mc.parent(arm, finger_group_name)
                mc.parent(thumb, finger_group_name)
                mc.parent(index, finger_group_name)
                mc.parent(mid, finger_group_name)
                mc.parent(ring, finger_group_name)
                mc.parent(pinky, finger_group_name)
                mc.parent(finger_group_name, setup)

                print(
                    f"'{l_arm_group_exists}' and '{l_thumb_group_exists}' and '{l_index_group_exists}' and '{l_mid_group_exists}' and '{l_ring_group_exists}' and '{l_pinky_group_exists}'  have been parented under '{setup}'.")
            else:
                missing_groups = []
                if not l_arm_group_exists:
                    missing_groups.append(arm)
                if not l_thumb_group_exists:
                    missing_groups.append(thumb)
                if not l_index_group_exists:
                    missing_groups.append(index)
                if not l_mid_group_exists:
                    missing_groups.append(mid)
                if not l_ring_group_exists:
                    missing_groups.append(ring)
                if not l_pinky_group_exists:
                    missing_groups.append(pinky)
                print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")

            # Function to create control structure for a joint
            def create_control_structure(joint_name, control_type):
                # Define suffixes
                #suffix = "_ctrl"
                #group_suffix = "_offset_grp"

                # Create two empty groups with specified suffixes
                group1 = mc.group(em=True, name=joint_name + '_grp')
                group2 = mc.group(em=True, name=joint_name + group_suffix)

                # Parent group2 under group1
                mc.parent(group2, group1)

                # Load the control from the JSON file
                try:
                    control_name = CPsLoadFromJson(control_type, ma_file_path)
                    print(f"Loaded control: {control_name}")

                    # Check if control_name is a valid object in the scene
                    if not mc.objExists(control_name):
                        raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                    # Parent the control under group2
                    mc.parent(control_name, group2)
                    print(f"Control {control_name} parented under {group2}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                # Define the names
                old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
                new_object_name = joint_name + suffix

                mc.select(old_object_name)
                mc.scale(10, 10, 10, old_object_name)
                mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

                # Rename the object
                if mc.objExists(old_object_name):
                    renamed_object = mc.rename(old_object_name, new_object_name)

                    # Create the group name
                    group_name = joint_name + group_suffix

                    # Check if the group already exists, if not, create it
                    if not mc.objExists(group_name):
                        group_name = mc.group(empty=True, name=group_name)

                    # Parent the renamed object under the group
                    mc.parent(renamed_object, group_name)

                    print(
                        f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
                else:
                    print(f"Object '{old_object_name}' does not exist in the scene.")

                # Match the transformation of group1 to the joint
                mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

                return group1, new_object_name

            # Define the root joints
            root_joint = 'FK_Shoulder_L'
            clav_joint = 'FK_Scapula_L'

            # Get all the children of the root joints
            all_children = mc.listRelatives(root_joint, allDescendents=True)
            all_joints = [root_joint] + all_children
            all_clav_joints = [clav_joint]

            # Dictionary to store the top group for each joint
            #joint_group_mapping = {}

            # Iterate through all joints and create control structures for FK controllers
            for joint in all_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            # Iterate through all clavicle joints and create control structures for Clav controllers
            for joint in all_clav_joints:
                group, control = create_control_structure(joint, "Clav_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            # Define the specific parent scheme
            parent_scheme = {
                'FK_Shoulder_L_grp': 'FK_Scapula_L',
                'FK_Elbow_L_grp': 'FK_Shoulder_L',
                'FK_Wrist_L_grp': 'FK_Elbow_L',

            }

            # Apply the parent scheme
            for child, parent in parent_scheme.items():
                if mc.objExists(child) and mc.objExists(parent):
                    mc.parent(child, parent)
                    print(f"{child} parented to {parent}")
                else:
                    print(f"Skipping {child} -> {parent} as one of them does not exist.")

        CPsFKArmCtrlL()

        def CPsFKArmCtrlR():

            # Define the objects
            arm = "FK_Scapula_R"
            root = "FK_Chest"
            wrist_joint = 'FK_Wrist_R'
            thumb = "FK_ThumbFinger1_R"
            index = "FK_IndexFinger0_R"
            mid = "FK_MiddleFinger0_R"
            ring = "FK_RingFinger0_R"
            pinky = "FK_PinkyFinger0_R"
            setup = "FK_Setup"
            finger_group_name = 'FKParentToWrist_R'

            l_arm_group_exists = mc.objExists(arm)
            l_thumb_group_exists = mc.objExists(thumb)
            l_index_group_exists = mc.objExists(index)
            l_mid_group_exists = mc.objExists(mid)
            l_ring_group_exists = mc.objExists(ring)
            l_pinky_group_exists = mc.objExists(pinky)

            if l_arm_group_exists and l_thumb_group_exists and l_index_group_exists and l_mid_group_exists and l_ring_group_exists and l_pinky_group_exists:
                # Create the main group
                main_finger_group = mc.group(empty=True, name=finger_group_name)

                # Get the transformation matrix of the root joint
                transform_matrix = mc.xform(wrist_joint, query=True, matrix=True, worldSpace=True)

                # Apply the transformation matrix to the main group
                mc.xform(main_finger_group, matrix=transform_matrix, worldSpace=True)

                # Parent the existing groups under the main group
                mc.parent(arm, finger_group_name)
                mc.parent(thumb, finger_group_name)
                mc.parent(index, finger_group_name)
                mc.parent(mid, finger_group_name)
                mc.parent(ring, finger_group_name)
                mc.parent(pinky, finger_group_name)
                mc.parent(finger_group_name, setup)

                print(
                    f"'{l_arm_group_exists}' and '{l_thumb_group_exists}' and '{l_index_group_exists}' and '{l_mid_group_exists}' and '{l_ring_group_exists}' and '{l_pinky_group_exists}'  have been parented under '{setup}'.")
            else:
                missing_groups = []
                if not l_arm_group_exists:
                    missing_groups.append(arm)
                if not l_thumb_group_exists:
                    missing_groups.append(thumb)
                if not l_index_group_exists:
                    missing_groups.append(index)
                if not l_mid_group_exists:
                    missing_groups.append(mid)
                if not l_ring_group_exists:
                    missing_groups.append(ring)
                if not l_pinky_group_exists:
                    missing_groups.append(pinky)
                print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")

            # Function to create control structure for a joint
            def create_control_structure(joint_name, control_type):


                # Create two empty groups with specified suffixes
                group1 = mc.group(em=True, name=joint_name + '_grp')
                group2 = mc.group(em=True, name=joint_name + group_suffix)

                # Parent group2 under group1
                mc.parent(group2, group1)

                # Load the control from the JSON file
                try:
                    control_name = CPsLoadFromJson(control_type, ma_file_path)
                    print(f"Loaded control: {control_name}")

                    # Check if control_name is a valid object in the scene
                    if not mc.objExists(control_name):
                        raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                    # Parent the control under group2
                    mc.parent(control_name, group2)
                    print(f"Control {control_name} parented under {group2}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                # Define the names
                old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
                new_object_name = joint_name + suffix

                mc.select(old_object_name)
                mc.scale(10, 10, 10, old_object_name)
                mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

                # Rename the object
                if mc.objExists(old_object_name):
                    renamed_object = mc.rename(old_object_name, new_object_name)

                    # Create the group name
                    group_name = joint_name + group_suffix

                    # Check if the group already exists, if not, create it
                    if not mc.objExists(group_name):
                        group_name = mc.group(empty=True, name=group_name)

                    # Parent the renamed object under the group
                    mc.parent(renamed_object, group_name)

                    print(
                        f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
                else:
                    print(f"Object '{old_object_name}' does not exist in the scene.")

                # Match the transformation of group1 to the joint
                mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

                return group1, new_object_name

            # Define the root joints
            root_joint = 'FK_Shoulder_R'
            clav_joint = 'FK_Scapula_R'

            # Get all the children of the root joints
            all_children = mc.listRelatives(root_joint, allDescendents=True)
            all_joints = [root_joint] + all_children
            all_clav_joints = [clav_joint]


            # Iterate through all joints and create control structures for FK controllers
            for joint in all_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            # Iterate through all clavicle joints and create control structures for Clav controllers
            for joint in all_clav_joints:
                group, control = create_control_structure(joint, "Clav_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            # Define the specific parent scheme
            parent_scheme = {
                'FK_Shoulder_R_grp': 'FK_Scapula_R',
                'FK_Elbow_R_grp': 'FK_Shoulder_R',
                'FK_Wrist_R_grp': 'FK_Elbow_R',

            }

            # Apply the parent scheme
            for child, parent in parent_scheme.items():
                if mc.objExists(child) and mc.objExists(parent):
                    mc.parent(child, parent)
                    print(f"{child} parented to {parent}")
                else:
                    print(f"Skipping {child} -> {parent} as one of them does not exist.")

        CPsFKArmCtrlR()

        # Define the names of the groups and joint
        existing_L_group = 'FK_Scapula_L_grp'
        existing_R_group = 'FK_Scapula_R_grp'
        existing_FK_group = 'FK_Setup'
        main_group_name = 'FKParentToChest'
        root_joint = 'FK_Chest'

        # Check if the existing groups and root joint exist
        l_group_exists = mc.objExists(existing_L_group)
        r_group_exists = mc.objExists(existing_R_group)
        fk_setup_group_exists = mc.objExists(existing_FK_group)
        root_joint_exists = mc.objExists(root_joint)

        if l_group_exists and r_group_exists and root_joint_exists and fk_setup_group_exists:
            # Create the main group
            main_group = mc.group(empty=True, name=main_group_name)

            # Get the transformation matrix of the root joint
            transform_matrix = mc.xform(root_joint, query=True, matrix=True, worldSpace=True)

            # Apply the transformation matrix to the main group
            mc.xform(main_group, matrix=transform_matrix, worldSpace=True)

            # Parent the existing groups under the main group
            mc.parent(existing_L_group, main_group)
            mc.parent(existing_R_group, main_group)
            mc.parent(main_group, existing_FK_group)

            print(f"'{existing_L_group}' and '{existing_R_group}' have been parented under '{main_group}'.")
        else:
            missing_groups = []
            if not l_group_exists:
                missing_groups.append(existing_L_group)
            if not r_group_exists:
                missing_groups.append(existing_R_group)
            if not root_joint_exists:
                missing_groups.append(root_joint)
            print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")

    CPsFKArmCtrl()

    def CPsFKNeckCtrl():
        # Define the objects
        neck = "FK_Neck"
        root = "FK_Chest"
        setup = "FK_Setup"

        # Unparent "FK_Hip_R" from "FK_Root"
        mc.parent(neck, setup)

        # Function to create control structure for a joint
        def create_control_structure(joint_name, control_type):

            # Create two empty groups with specified suffixes
            group1 = mc.group(em=True, name=joint_name + '_grp')
            group2 = mc.group(em=True, name=joint_name + group_suffix)

            # Parent group2 under group1
            mc.parent(group2, group1)

            # Load the control from the JSON file
            try:
                control_name = CPsLoadFromJson(control_type, ma_file_path)
                print(f"Loaded control: {control_name}")

                # Check if control_name is a valid object in the scene
                if not mc.objExists(control_name):
                    raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                # Parent the control under group2
                mc.parent(control_name, group2)
                print(f"Control {control_name} parented under {group2}")

            except Exception as e:
                print(f"An error occurred: {e}")

            # Define the names
            old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
            new_object_name = joint_name + suffix

            mc.select(old_object_name)
            mc.scale(10, 10, 10, old_object_name)
            mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

            # Rename the object
            if mc.objExists(old_object_name):
                renamed_object = mc.rename(old_object_name, new_object_name)

                # Create the group name
                group_name = joint_name + group_suffix

                # Check if the group already exists, if not, create it
                if not mc.objExists(group_name):
                    group_name = mc.group(empty=True, name=group_name)

                # Parent the renamed object under the group
                mc.parent(renamed_object, group_name)

                print(
                    f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
            else:
                print(f"Object '{old_object_name}' does not exist in the scene.")

            # Match the transformation of group1 to the joint
            mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

            return group1, new_object_name

        # Define the root joints
        root_joint = 'FK_Neck'
        head_joint = 'FK_Head'

        all_joints = [root_joint]
        all_Head_joints = [head_joint]


        # Iterate through all joints and create control structures for FK controllers
        for joint in all_joints:
            group, control = create_control_structure(joint, "FK_controller")
            joint_group_mapping[joint] = group
            mc.parent(joint, control)
            print(f"Joint {joint} parented to control {control}")

        # Iterate through all clavicle joints and create control structures for Clav controllers
        for joint in all_Head_joints:
            group, control = create_control_structure(joint, "IK_controller")
            joint_group_mapping[joint] = group
            mc.parent(joint, control)
            print(f"Joint {joint} parented to control {control}")

        # Define the specific parent scheme
        parent_scheme = {
            'FK_Head_grp': 'FK_Neck',
        }
        # Apply the parent scheme
        for child, parent in parent_scheme.items():
            if mc.objExists(child) and mc.objExists(parent):
                mc.parent(child, parent)
                print(f"{child} parented to {parent}")
            else:
                print(f"Skipping {child} -> {parent} as one of them does not exist.")

        existing_neck_group = 'FK_Neck_grp'
        existing_FK_group = 'FK_Setup'
        existing_group = 'FKParentToChest'
        neck_group_exists = mc.objExists(existing_neck_group)
        fk_setup_group_exists = mc.objExists(existing_FK_group)
        fk_group_exists = mc.objExists(existing_group)
        if neck_group_exists and fk_setup_group_exists and fk_group_exists:
            mc.parent(existing_neck_group, existing_group)
                    #mc.parent(existing_group, existing_FK_group)

            print(f"'{existing_neck_group}' have been parented under '{existing_group}'.")
        else:
            missing_groups = []
            if not neck_group_exists:
                missing_groups.append(existing_neck_group)


            print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")

    CPsFKNeckCtrl()

    def CPsFKHandCtrl():

        def CPsFKFingerCtrl():

            # Define the objects
            thumb_L = "FK_ThumbFinger1_L"
            index_L = "FK_IndexFinger0_L"
            mid_L = "FK_MiddleFinger0_L"
            ring_L = "FK_RingFinger0_L"
            pinky_L = "FK_PinkyFinger0_L"

            thumb_R = "FK_ThumbFinger1_R"
            index_R = "FK_IndexFinger0_R"
            mid_R = "FK_MiddleFinger0_R"
            ring_R = "FK_RingFinger0_R"
            pinky_R = "FK_PinkyFinger0_R"


            # Function to create control structure for a joint
            def create_control_structure(joint_name, control_type):

                # Create two empty groups with specified suffixes
                group1 = mc.group(em=True, name=joint_name + '_grp')
                group2 = mc.group(em=True, name=joint_name + group_suffix)

                # Parent group2 under group1
                mc.parent(group2, group1)

                # Load the control from the JSON file
                try:
                    control_name = CPsLoadFromJson(control_type, ma_file_path)
                    print(f"Loaded control: {control_name}")

                    # Check if control_name is a valid object in the scene
                    if not mc.objExists(control_name):
                        raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                    # Parent the control under group2
                    mc.parent(control_name, group2)
                    print(f"Control {control_name} parented under {group2}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                # Define the names
                old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
                new_object_name = joint_name + suffix

                mc.select(old_object_name)
                mc.scale(2, 2, 2, old_object_name)
                mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

                # Rename the object
                if mc.objExists(old_object_name):
                    renamed_object = mc.rename(old_object_name, new_object_name)

                    # Create the group name
                    group_name = joint_name + group_suffix

                    # Check if the group already exists, if not, create it
                    if not mc.objExists(group_name):
                        group_name = mc.group(empty=True, name=group_name)

                    # Parent the renamed object under the group
                    mc.parent(renamed_object, group_name)

                    print(
                        f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
                else:
                    print(f"Object '{old_object_name}' does not exist in the scene.")

                # Match the transformation of group1 to the joint
                mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

                return group1, new_object_name

            # Define the root joints


            all_thumb_L_joints = [thumb_L] + mc.listRelatives(thumb_L, allDescendents=True)
            all_index_L_joints = [index_L] + mc.listRelatives(index_L, allDescendents=True)
            all_mid_L_joints = [mid_L] + mc.listRelatives(mid_L, allDescendents=True)
            all_ring_L_joints = [ring_L] + mc.listRelatives(ring_L, allDescendents=True)
            all_pinky_L_joints = [pinky_L] + mc.listRelatives(pinky_L, allDescendents=True)

            all_thumb_R_joints = [thumb_R] + mc.listRelatives(thumb_R, allDescendents=True)
            all_index_R_joints = [index_R] + mc.listRelatives(index_R, allDescendents=True)
            all_mid_R_joints = [mid_R] + mc.listRelatives(mid_R, allDescendents=True)
            all_ring_R_joints = [ring_R] + mc.listRelatives(ring_R, allDescendents=True)
            all_pinky_R_joints = [pinky_R] + mc.listRelatives(pinky_R, allDescendents=True)



            # Dictionary to store the top group for each joint

            for joint in all_thumb_L_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_index_L_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_mid_L_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_ring_L_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_pinky_L_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_thumb_R_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_index_R_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_mid_R_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_ring_R_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")

            for joint in all_pinky_R_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")



            # Define the specific parent scheme
            parent_scheme = {
                'FK_ThumbFinger2_L_grp': 'FK_ThumbFinger1_L',
                'FK_ThumbFinger3_L_grp': 'FK_ThumbFinger2_L',

                'FK_IndexFinger1_L_grp': 'FK_IndexFinger0_L',
                'FK_IndexFinger2_L_grp': 'FK_IndexFinger1_L',
                'FK_IndexFinger3_L_grp': 'FK_IndexFinger2_L',

                'FK_MiddleFinger1_L_grp': 'FK_MiddleFinger0_L',
                'FK_MiddleFinger2_L_grp': 'FK_MiddleFinger1_L',
                'FK_MiddleFinger3_L_grp': 'FK_MiddleFinger2_L',

                'FK_RingFinger1_L_grp': 'FK_RingFinger0_L',
                'FK_RingFinger2_L_grp': 'FK_RingFinger1_L',
                'FK_RingFinger3_L_grp': 'FK_RingFinger2_L',

                'FK_PinkyFinger1_L_grp': 'FK_PinkyFinger0_L',
                'FK_PinkyFinger2_L_grp': 'FK_PinkyFinger1_L',
                'FK_PinkyFinger3_L_grp': 'FK_PinkyFinger2_L',

                'FK_ThumbFinger2_R_grp': 'FK_ThumbFinger1_R',
                'FK_ThumbFinger3_R_grp': 'FK_ThumbFinger2_R',

                'FK_IndexFinger1_R_grp': 'FK_IndexFinger0_R',
                'FK_IndexFinger2_R_grp': 'FK_IndexFinger1_R',
                'FK_IndexFinger3_R_grp': 'FK_IndexFinger2_R',

                'FK_MiddleFinger1_R_grp': 'FK_MiddleFinger0_R',
                'FK_MiddleFinger2_R_grp': 'FK_MiddleFinger1_R',
                'FK_MiddleFinger3_R_grp': 'FK_MiddleFinger2_R',

                'FK_RingFinger1_R_grp': 'FK_RingFinger0_R',
                'FK_RingFinger2_R_grp': 'FK_RingFinger1_R',
                'FK_RingFinger3_R_grp': 'FK_RingFinger2_R',

                'FK_PinkyFinger1_R_grp': 'FK_PinkyFinger0_R',
                'FK_PinkyFinger2_R_grp': 'FK_PinkyFinger1_R',
                'FK_PinkyFinger3_R_grp': 'FK_PinkyFinger2_R',


            }

            # Apply the parent scheme
            for child, parent in parent_scheme.items():
                if mc.objExists(child) and mc.objExists(parent):
                    mc.parent(child, parent)
                    print(f"{child} parented to {parent}")
                else:
                    print(f"Skipping {child} -> {parent} as one of them does not exist.")

        CPsFKFingerCtrl()

        # Define the names of the groups and joint
        existing_Hand_L_group = ['FK_ThumbFinger1_L_grp',
                                 'FK_IndexFinger0_L_grp',
                                 'FK_MiddleFinger0_L_grp',
                                 'FK_RingFinger0_L_grp',
                                 'FK_PinkyFinger0_L_grp'
                                 ]

        existing_Hand_R_group = ['FK_ThumbFinger1_R_grp',
                                 'FK_IndexFinger0_R_grp',
                                 'FK_MiddleFinger0_R_grp',
                                 'FK_RingFinger0_R_grp',
                                 'FK_PinkyFinger0_R_grp'
                                 ]
        existing_FK_group = 'FK_Setup'
        existing_l_hand_grp = 'FKParentToWrist_L'
        existing_r_hand_grp = 'FKParentToWrist_R'
        l_hand_group_exists = all(mc.objExists(group) for group in existing_Hand_L_group)
        r_hand_group_exists = all(mc.objExists(group) for group in existing_Hand_R_group)
        l_hand_grp_exists = mc.objExists(existing_l_hand_grp)
        r_hand_grp_exists = mc.objExists(existing_r_hand_grp)


        if l_hand_group_exists and r_hand_group_exists and existing_FK_group and l_hand_grp_exists and r_hand_grp_exists:

            for group in existing_Hand_L_group:
                mc.parent(group, existing_l_hand_grp)
                print(f"{group} parented to {existing_l_hand_grp}.")

            for group in existing_Hand_R_group:
                mc.parent(group, existing_r_hand_grp)
                print(f"{group} parented to {existing_r_hand_grp}.")

        else:
            missing_groups = []
            if not l_hand_grp_exists:
                missing_groups.append(existing_l_hand_grp)
            if not r_hand_grp_exists:
                missing_groups.append(existing_r_hand_grp)
            if not l_hand_group_exists:
                missing_groups.extend(existing_Hand_L_group)
            if not r_hand_group_exists:
                missing_groups.extend(existing_Hand_R_group)

            print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")

    CPsFKHandCtrl()

    def CPsFkRootCtrl():
        def CPsFKSpineCtrl():

            # Define group names
            root_joint = 'FK_Root'
            spine_joint = 'FK_Spine1'
            toRoot = "IKToRoot"
            toSpine1 = "FKToRoot"
            toSpine2 = "FKToSpine1"
            hipSway = "HipSway"
            hipSwaySTT = "HipSwayStableTarget"
            hipSwayST = "HipSwayStable"
            reverseHip = "ReverseHipSway"
            hipToRoot = "ReverseHipToRoot"

            group3 = mc.group(em=True, name=toSpine1)
            group4 = mc.group(em=True, name=toSpine2)
            group5 = mc.group(em=True, name=hipSway)
            group6 = mc.group(em=True, name=hipToRoot)
            group7 = mc.group(em=True, name=hipSwayST)
            group8 = mc.group(em=True, name=reverseHip)
            group9 = mc.group(em=True, name=toRoot)
            group10 = mc.group(em=True, name=hipSwaySTT)

            def CPsCreateGroupJtLoc():
                if not mc.objExists(root_joint):
                    mc.error(f"Joint {root_joint} does not exist in the scene.")
                    return

                if not mc.objExists(spine_joint):
                    mc.error(f"Joint {spine_joint} does not exist in the scene.")
                    return
                transform_root_matrix = mc.xform(root_joint, query=True, matrix=True, worldSpace=True)
                transform_spine_matrix = mc.xform(spine_joint, query=True, matrix=True, worldSpace=True)

                groupRoots = [
                    group3, group6, group9
                ]
                groupSpines = [
                    group5, group4, group7, group8, group10
                ]

                for groupRoot in groupRoots:
                    if mc.objExists(groupRoot):
                        mc.xform(groupRoot, matrix=transform_root_matrix, worldSpace=True)
                        mc.makeIdentity(groupRoot, apply=True, translate=True, rotate=True, scale=True, normal=False)

                        print(f"Created and froze transformations for group '{groupRoot}' at the location.")
                    else:
                        print(f"Group '{groupRoot}' does not exist in the scene")

                for groupSpine in groupSpines:
                    if mc.objExists(groupSpine):
                        mc.xform(groupSpine, matrix=transform_spine_matrix, worldSpace=True)
                        mc.makeIdentity(groupSpine, apply=True, translate=True, rotate=True, scale=True, normal=False)

                        print(f"Created and froze transformations for group '{groupSpine}' at the location.")
                    else:
                        print(f"Group '{groupSpine}' does not exist in the scene")

            CPsCreateGroupJtLoc()

            # Function to create control structure for a joint
            def create_control_structure(joint_name, control_type):
                # Create groups
                group1 = mc.group(em=True, name=joint_name + '_grp')
                group2 = mc.group(em=True, name=joint_name + group_suffix)


                # Parent group2 under group1
                mc.parent(group2, group1)



                # Load the control from the JSON file
                try:
                    control_name = CPsLoadFromJson(control_type, ma_file_path)
                    print(f"Loaded control: {control_name}")

                    # Check if control_name is a valid object in the scene
                    if not mc.objExists(control_name):
                        raise RuntimeError(f"Control {control_name} does not exist in the scene after loading.")

                    # Parent the control under group2
                    mc.parent(control_name, group2)
                    print(f"Control {control_name} parented under {group2}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                # Define the names
                old_object_name = "_UNKNOWN_REF_NODE_fosterParent1"
                new_object_name = joint_name + suffix

                mc.select(old_object_name)
                mc.scale(10, 10, 10, old_object_name)
                mc.makeIdentity(old_object_name, apply=True, t=1, r=1, s=1, n=0)

                # Rename the object
                if mc.objExists(old_object_name):
                    renamed_object = mc.rename(old_object_name, new_object_name)

                    group_name = joint_name + group_suffix

                    if not mc.objExists(group_name):
                        group_name = mc.group(empty=True, name=group_name)

                    mc.parent(renamed_object, group_name)

                    print(
                        f"Object '{old_object_name}' has been renamed to '{new_object_name}' and parented under group '{group_name}'")
                else:
                    print(f"Object '{old_object_name}' does not exist in the scene.")

                # Match the transformation of group1 to the joint
                mc.xform(group1, ws=True, matrix=mc.xform(joint_name, q=True, ws=True, matrix=True))

                return group1, new_object_name

            def CPsCreateHipsway_IK():
                hipsway_grp, control = create_control_structure(hipSway, "IK_controller")
                constraint = mc.parentConstraint(root_joint, hipsway_grp, mo=False) [0]
                print(f"Create IK controller for '{hipSway}' and inherit to the location the '{root_joint}")
                mc.delete(constraint)
                print(f"Deleted the parent constaint on '{hipSway}")

            CPsCreateHipsway_IK()

            all_children = mc.listRelatives(root_joint, allDescendents=True)
            all_spine_joints = [root_joint] + all_children
            #grpCtrl = [hipSway]

            for joint in all_spine_joints:
                group, control = create_control_structure(joint, "FK_controller")
                joint_group_mapping[joint] = group
                mc.parent(joint, control)
                print(f"Joint {joint} parented to control {control}")


            # Define the specific parent scheme (optional if needed)
            parent_scheme = {

                'IKToRoot': 'FK_Root',
                'HipSwayStableTarget': 'FK_Root',
                'ReverseHipSway': 'FK_Root',
                'ReverseHipToRoot': 'ReverseHipSway',
                'HipSway_grp': 'FK_Root',
                'FKToRoot': 'FK_Root',
                'FKToSpine1': 'FKToRoot',
                'HipSwayStable': 'HipSway',
                'HipSway': 'FK_Root',
                'FK_Spine1_grp': 'HipSwayStable',
                'FK_Spine2_grp': 'FK_Spine1',
                'FK_Spine3_grp': 'FK_Spine2',
                'FK_Spine4_grp': 'FK_Spine3',
                'FK_Chest_grp': 'FK_Spine4'

            }

            # Apply the parent scheme (if defined)
            for child, parent in parent_scheme.items():
                if mc.objExists(child) and mc.objExists(parent):
                    mc.parent(child, parent)
                    print(f"{child} parented to {parent}")
                else:
                    print(f"Skipping {child} -> {parent} as one of them does not exist.")

            # Define the names of the groups and joint
            existing_root_group = 'FK_Root_grp'
            existing_FK_group = 'FK_Setup'
            root_group_name = 'FKToRoot'
            root_joint = 'FK_Root'

            # Check if the existing groups and root joint exist
            root_group_exists = mc.objExists(existing_root_group)
            fk_setup_group_exists = mc.objExists(existing_FK_group)
            root_joint_exists = mc.objExists(root_joint)

            if root_group_exists and root_joint_exists and fk_setup_group_exists:
                # Create the main group
                main_group = mc.group(empty=True, name=root_group_name)

                transform_matrix = mc.xform(root_joint, query=True, matrix=True, worldSpace=True)
                mc.xform(main_group, matrix=transform_matrix, worldSpace=True)

                mc.parent(existing_root_group, main_group)
                mc.parent(main_group, existing_FK_group)

                print(f"'{existing_root_group}' have been parented under '{main_group}'.")
            else:
                missing_groups = []
                if not root_group_exists:
                    missing_groups.append(existing_root_group)
                if not root_joint_exists:
                    missing_groups.append(root_joint)
                print(f"Group(s) or joint '{', '.join(missing_groups)}' do not exist.")

        CPsFKSpineCtrl()



    CPsFkRootCtrl()
