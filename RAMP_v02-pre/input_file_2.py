# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''

def input_file(arch,prov):
    
    from core import User, np, pd
    User_list = []
    k = arch
    p = prov
    
    #Timeseries for DHW tasks median power
    T_gw = pd.read_csv('time_series/gw_temp_province.csv', sep=';', index_col=0, usecols=['day',p])
    
    shower_P = 8/60*4186*(45-T_gw)
    sink_P = 4/60*4186*(40-T_gw)
    kitchen_P = 5/60*4186*(40-T_gw)
    generic_P = 4/60*4186*(40-T_gw)
    
    #Create new user classes
    U2 = User("User type 2",1)
    User_list.append(U2)

#    User type 2
    U2_shower_wd = U2.Appliance(U2,1,shower_P,2,8*k,0.2,3, thermal_P_var = 0.2, P_series=True, wd_we_type=0)
    U2_shower_wd.windows([360,1080],[960,1380],0.2)
    
    U2_shower_we = U2.Appliance(U2,1,shower_P,2,8*k,0.2,3, thermal_P_var = 0.2, P_series=True, wd_we_type=1)
    U2_shower_we.windows([360,660],[1020,1380],0.2)
    
    U2_sink_wd = U2.Appliance(U2,1,sink_P,2,3*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=0)
    U2_sink_wd.windows([360,540],[960,1380],0.2)
    
    U2_sink_we = U2.Appliance(U2,1,sink_P,1,3*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=1)
    U2_sink_we.windows([420,1380],[0,0],0.2)
    
    U2_kitchen_wd = U2.Appliance(U2,1,kitchen_P,2,5*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=0)
    U2_kitchen_wd.windows([360,540],[960,1380],0.2)
    
    U2_kitchen_we = U2.Appliance(U2,1,kitchen_P,1,5*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=1)
    U2_kitchen_we.windows([420,1380],[0,0],0.2)
    
    U2_generic_wd = U2.Appliance(U2,1,generic_P,1,2*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=0)
    U2_generic_wd.windows([0,1440],[0,0],0)
    
    U2_generic_we = U2.Appliance(U2,1,generic_P,1,2*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=1)
    U2_generic_we.windows([0,1440],[0,0],0)
    
    return(User_list)