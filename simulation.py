import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        self.logger = Logger('log.txt')
        self.population = [] # List of Person objects
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.newly_infected = []
        self.newly_dead=0
        self.number_infected=0

    def _create_population(self, initial_infected):
        for i in range(0,self.pop_size):
            amt_vaccinated=int(round(self.pop_size*self.vacc_percentage))
            if i<=amt_vaccinated:
                self.population.append(Person(self.next_person_id,True,None))
            elif i>amt_vaccinated and i<=amt_vaccinated+initial_infected:
                self.population.append(Person(self.next_person_id,False,self.virus))
            else:
                self.population.append(Person(self.next_person_id,False,None))
            self.next_person_id+=1

    def _simulation_should_continue(self):
        for person in self.population:
            if not person.infection==None:
                return True
        return False

    def run(self):
        print(f"=== Simulation Begins ===")
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            print(f"Running time step {time_step_counter}.")
            self.time_step()
            self._infect_newly_infected()
            self.logger.log_time_step(time_step_counter,len(self.newly_infected),self.newly_dead,self.total_infected,self.total_dead)
            should_continue = self._simulation_should_continue()
            time_step_counter+=1
            print(f"{str(len(self.newly_infected))} infected by {str(self.number_infected)} people, {str(self.newly_dead)} of which died.")
        print(f"=== Simulation Completed After {str(time_step_counter)} Steps ===")
        print(f"Full log in log.txt")

    def time_step(self):
        self.newly_infected=[]
        self.newly_dead=0
        self.number_infected=0
        for person in self.population:
            if not person.infection==None:
                self.number_infected+=1
                live_population_without_person=[] # People can't interact with themselves or dead people
                for other_person in self.population:
                    if not other_person._id==person._id and other_person.is_alive==True:
                        live_population_without_person.append(other_person)
                self.interaction(person, random.sample(live_population_without_person, 100))
                dice_roll=random.uniform(0,1)
                if dice_roll<=self.virus.mortality_rate:
                    person.infection=None
                    person.is_alive=False
                    self.newly_dead+=1
                    self.logger.log_infection_survival(person,True)
                else:
                    person.is_vaccinated=True
                    person.infection=None
                    self.logger.log_infection_survival(person,False)
        self.total_dead+=self.newly_dead
        self.total_infected+=len(self.newly_infected)

    def interaction(self, person, random_people_list):
        for random_person in random_people_list:
            if random_person.is_vaccinated==False:
                if random_person.infection==None and random_person not in self.newly_infected: # If they're healthy but unvaccinated
                    dice_roll=random.uniform(0,1)
                    if dice_roll<=self.virus.repro_rate:
                        self.newly_infected.append(random_person)
                        self.logger.log_interaction(person, random_person, False,False,True)
                    else:
                        self.logger.log_interaction(person,random_person,False,False,False)
                else:
                    self.logger.log_interaction(person, random_person, True, False, False)
                assert person.is_alive==True
                assert random_person.is_alive == True
            else:
                self.logger.log_interaction(person, random_person, False, True, False)

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection=self.virus

if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size,vacc_percentage,virus,initial_infected)
    sim.logger.write_metadata(pop_size,vacc_percentage,virus_name,mortality_rate,repro_rate)
    sim._create_population(initial_infected)
    sim.run()
