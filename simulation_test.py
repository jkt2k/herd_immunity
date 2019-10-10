import unittest
from simulation import Simulation
from logger import Logger
from person import Person
from virus import Virus

def test_instantiation():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    assert sim.initial_infected==10
    assert sim.pop_size==10000
    assert sim.vacc_percentage==0.90

def test_create_population():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    sim._create_population(10)
    assert len(sim.population)==10000

def test_simulation_should_continue():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 0)
    sim.logger.write_metadata(10000, 0.90, "Ebola", 0.25, 0.70)
    sim._create_population(0)
    assert sim._simulation_should_continue()==False

def test_run():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    sim.logger.write_metadata(10000, 0.90, "Ebola", 0.25, 0.70)
    sim._create_population(10)
    sim.run()
    someone_died=False
    for person in sim.population:
        if person.is_alive==False:
            someone_died=True
    assert someone_died==True
