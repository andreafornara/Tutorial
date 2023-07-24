def set_BB(collider, beam = 'lhcb1', bb_lr = False, HO_1 = False, HO_2 = False, HO_5 = False, HO_8 = False):
    if bb_lr == False:
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_lr')]
        print('Removed BB LR from line '+beam)
    start_len = len(collider[beam].element_names)
    if(HO_5 == False):
        print('Removing HO lenses at IP5')
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.l5')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.c5')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.r5')]
    if(HO_8 == False):
        print('Removing HO lenses at IP8')
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.l8')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.c8')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.r8')]
    if(HO_2 == False):
        print('Removing HO lenses at IP2')
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.l2')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.c2')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.r2')]
    if(HO_1 == False):
        print('Removing HO lenses at IP1')
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.l1')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.c1')]
        collider[beam].element_names = [element for element in collider[beam].element_names if not element.startswith('bb_ho.r1')]

    for element in collider[beam].element_names:
        if element.startswith('bb_ho'):
            print('Problem: the following lenses have not been removed:')
            if ((element.endswith('_12')) or (element.endswith('_05')) or 
                (element.endswith('_04')) or (element.endswith('_03')) or 
                (element.endswith('_02')) or ((element.endswith('_01')))):
                # collider[beam].element_names.remove(element)
                print(element)
    end_len = len(collider[beam].element_names)
    if(start_len != end_len):
        print(f'HO lenses removed = {start_len-end_len}')
    return collider
def set_orbit_flat(collider):
    print('Setting optics as flat')
    for ii in ['on_x1', 'on_sep1', 'on_x2', 'on_sep2', 'on_x5',
               'on_sep5', 'on_x8h', 'on_x8v', 'on_sep8h', 'on_sep8v',
               'on_a1', 'on_o1', 'on_a2', 'on_o2', 'on_a5', 'on_o5', 'on_a8', 
               'on_o8', 'on_disp', 'on_crab1', 'on_crab5', 'on_alice_normalized', 
               'on_lhcb_normalized', 'on_sol_atlas', 'on_sol_cms', 'on_sol_alice', 
               'i_oct_b1', 'i_oct_b2']:
        collider.vars[ii] = 0
    return collider
def set_orbit_from_config(collider, config):
    print('Setting optics as from config')
    for ii in ['on_x1', 'on_sep1', 'on_x2', 'on_sep2', 'on_x5',
               'on_sep5', 'on_x8h', 'on_x8v', 'on_sep8h', 'on_sep8v',
               'on_a1', 'on_o1', 'on_a2', 'on_o2', 'on_a5', 'on_o5', 'on_a8', 
               'on_o8', 'on_disp', 'on_crab1', 'on_crab5', 'on_alice_normalized', 
               'on_lhcb_normalized', 'on_sol_atlas', 'on_sol_cms', 'on_sol_alice', 
               'vrf400', 'lagrf400.b1', 'lagrf400.b2', 'i_oct_b1', 'i_oct_b2']:
        collider.vars[ii] = config['config_collider']['config_knobs_and_tuning']['knob_settings'][ii]
    return collider