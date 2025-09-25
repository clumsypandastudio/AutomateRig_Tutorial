import maya.cmds as mc

def CPsSetupStructure():
    def CPsCreateGroups(*args):
        group_name = mc.textField(name_field, query=True, text=True)
        if group_name:

            #Create new grps
            controls_group = mc.group(empty=True, name="Controls_Setup")

            def CPsControlsSystem(controlsSetup, mainSetup):
                controlsGroups =[]
                for name in controlsSetup:
                    group = mc.group(empty=True, name=name)
                    controlsGroups.append(group)
                    print(f"Group '{name}' created")

                mainGroups =[]
                for name in mainSetup:
                    group = mc.group(empty=True, name=name)
                    mainGroups.append(group)
                    print(f"Group '{name}' created")
                
                return controlsGroups, mainGroups

            controlsSetup = ['Skeleton_Setup', 'Mesh', 'Extra']
            mainSetup = ['Main_Setup', 
                         'FK_Setup', 
                         'IK_Setup', 
                         'IK_FK_Switch_Setup', 
                         'BlendShape_Setup', 
                         'Aim_Setup',
                         'Twist_Setup',
                         'Root_Setup', 
                         'Global_Setup', 
                         'Constraint_Setup', 
                         'Dynamic_Setup', 
                         'SetDriver_Setup'
                         ]

            #Create the Groups

            controlsGroups, mainGroups = CPsControlsSystem(controlsSetup, mainSetup)

            top_Node = mc.group(empty=True, name=group_name)

            mc.parent (controls_group, top_Node)
            mc.parent (controlsGroups, top_Node)
            mc.parent (mainGroups, controls_group)

        mc.deleteUI(window, window=True)

    window = mc.window(title= "Create Top Node")
    mc.columnLayout(adjustableColumn=True)
    mc.text(label="Enter the name for your character:")
    name_field = mc.textField()
    mc.button(label = "Create", command=CPsCreateGroups)
    mc.showWindow(window)
