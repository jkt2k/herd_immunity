import datetime
import os
class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name=os.path.dirname(os.path.realpath(__file__))+'/'+file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        with open(self.file_name,'w') as virus_log:
            virus_log.write(f"{str(datetime.datetime.now())}\n")
        virus_log.close()
        with open(self.file_name,'a') as virus_log:
            virus_log.write(f"Population size: {str(pop_size)}\n")
            virus_log.write(f"Percentage of population vaccinated: {str(vacc_percentage)}\n")
            virus_log.write(f"Pathogen name: {virus_name}\n")
            virus_log.write(f"Pathogen mortality rate: {str(mortality_rate)}\n")
            virus_log.write(f"Pathogen reproduction rate: {str(basic_repro_num)}\n")
            virus_log.write(f"=== Simulation Begins ===\n")
        virus_log.close()
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        pass

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        sequence=[random_person_sick,random_person_vacc,did_infect]
        if sequence==[False, False, True]:
            with open(self.file_name,'a') as virus_log:
                virus_log.write(f"{person._id} infected {random_person._id}.\n")
        elif sequence==[False, False, False]:
            with open(self.file_name,'a') as virus_log:
                virus_log.write(f"{person._id} interacted with {random_person._id} but luckily did not infect them.\n")
        elif sequence==[True, False, False]:
            with open(self.file_name,'a') as virus_log:
                virus_log.write(f"{person._id} interacted with {random_person._id}, who is already infected.\n")
        elif sequence==[False, True, False]:
            with open(self.file_name,'a') as virus_log:
                virus_log.write(f"{person._id} interacted with {random_person._id}, who is vaccinated.\n")

    def log_infection_survival(self, person, did_die_from_infection):
        if did_die_from_infection==True:
            with open(self.file_name,'a') as virus_log:
                virus_log.write(f"{person._id} died from infection.\n")
        else:
            with open(self.file_name,'a') as virus_log:
                virus_log.write(f"{person._id} survived infection.\n")

    def log_time_step(self, time_step_number, number_infected, number_died, total_infected, total_died):
        with open(self.file_name,'a') as virus_log:
            virus_log.write(f"Time step {str(time_step_number)} ended.\n")
            virus_log.write(f"Latest time step ({str(time_step_number)}): {str(number_infected)} infected, {str(number_died)} dead.\n")
            virus_log.write(f"Simulation: {str(total_infected)} infected, {str(total_died)} dead.\n")

logger=Logger('log.txt')
logger.write_metadata(100,90,"hey",50,50)