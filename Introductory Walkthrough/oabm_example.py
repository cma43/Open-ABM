from openabm import *

##############################################
#Import and run 
##############################################

env = make('Bank-Reserves', server = True)  
env.run_model()


##############################################
#Running the model
##############################################

# model_run = env.run_model(10)

# #Export and see head of sim data:
# model_data = export_model_data(model_run)
# print(model_data)

##############################################
#Adjusting model parameters
##############################################

# new_model_params = get_model_parameters(env)
# print(new_model_params)

# new_stuff = {'running': False}
# model = set_model_parameters(env, new_stuff)

# print(get_model_parameters(model))

##############################################
#Adjusting agent parameters
##############################################

# agent_params = get_agent_parameters(env)

# new_param = {0: {'moore':False}, 1: {'moore': False}}

# new_model = set_agent_parameters(env, new_param)

# print(get_agent_parameters(new_model)[1]['moore']) 
# print(get_agent_parameters(new_model)[0]['moore']) 

# new_param = {0: {'moore':False}, 1: {'moore': True}}
# new_model = set_agent_parameters(env, new_param)

# print(get_agent_parameters(new_model)[1]['moore']) 
# print(get_agent_parameters(new_model)[0]['moore']) 

##############################################
#Adjusting data collection
##############################################

# def get_total_savings(model):
#     """sum of all agents' savings"""

#     agent_savings = [a.savings for a in model.schedule.agents]
#     # return the sum of agents' savings
#     return np.sum(agent_savings)


# model_data = {"Savings": get_total_savings, 'Number Of Steps': 'num_steps'}
# env = set_data_collection(env, False, True, model_data_to_collect= model_data) #NOTE: important to specify _to_collect variant
# model_run = env.run_model(10)

# #Export and see head of sim data:
# model_data = export_model_data(model_run)
# print(model_data) 

##############################################
#Changing step() functions for agents/model
##############################################

# def new_step(self):
#     print('Success!')
#     return

#TODO: start by making function that takes a step function, assuming only random activation

# get_agent_step(env.schedule.agents)
# get_model_step(env)











