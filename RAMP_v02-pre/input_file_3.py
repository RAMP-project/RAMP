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
    
    shower_P = 8/60*4186*(40-T_gw)
    sink_P = 4/60*4186*(35-T_gw)
    kitchen_P = 5/60*4186*(40-T_gw)
    generic_P = 4/60*4186*(35-T_gw)
    
    #Create new user classes
    U3 = User("User type 3",1)
    User_list.append(U3)
    
    #User type 3
    U3_shower_wd = U3.Appliance(U3,1,shower_P,2,8*k,0.2,3, thermal_P_var = 0.1, P_series=True, wd_we_type=0)
    U3_shower_wd.windows([300,540],[1020,1320],0.3)
    
    U3_shower_we = U3.Appliance(U3,1,shower_P,2,8*k,0.2,3, thermal_P_var = 0.1, P_series=True, wd_we_type=1)
    U3_shower_we.windows([360,600],[840,1200],0.3)
    
    U3_sink_wd = U3.Appliance(U3,1,sink_P,1,4*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=0)
    U3_sink_wd.windows([360,1320],[0,0],0.3)
    
    U3_sink_we = U3.Appliance(U3,1,sink_P,1,4*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=1)
    U3_sink_we.windows([360,1320],[0,0],0.3)
    
    U3_kitchen_wd = U3.Appliance(U3,1,kitchen_P,2,5*k,0.2,1, thermal_P_var = 0.1, P_series=True, wd_we_type=0)
    U3_kitchen_wd.windows([360,540],[1020,1320],0.3)
    
    U3_kitchen_we = U3.Appliance(U3,1,kitchen_P,1,5*k,0.2,1, thermal_P_var = 0.1, P_series=True, wd_we_type=1)
    U3_kitchen_we.windows([360,1320],[0,0],0.3)
    
    U3_generic_wd = U3.Appliance(U3,1,generic_P,1,3*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=0)
    U3_generic_wd.windows([0,1440],[0,0],0)
    
    U3_generic_we = U3.Appliance(U3,1,generic_P,1,3*k,0.2,1, thermal_P_var = 0.25, P_series=True, wd_we_type=1)
    U3_generic_we.windows([0,1440],[0,0],0)
    
    return(User_list)