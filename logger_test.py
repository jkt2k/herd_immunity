import unittest
import os
from simulation import Simulation
from logger import Logger
from person import Person
from virus import Virus

def test_write_metadata():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    sim.logger.write_metadata(10000, 0.90, "Ebola", 0.25, 0.70)
    assert os.path.getsize(os.path.dirname(os.path.realpath(__file__))+'/log.txt')==200

def test_log_interaction():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    sim.logger.write_metadata(10000, 0.90, "Ebola", 0.25, 0.70)
    sim._create_population(10)
    sim.run()
    assert type(sim.logger)==Logger

def test_log_infection_survival():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    sim.logger.write_metadata(10000, 0.90, "Ebola", 0.25, 0.70)
    sim._create_population(10)
    sim.run()
    assert type(sim.logger)==Logger

def test_log_time_step():
    virus=Virus("Ebola",0.70,0.25)
    sim=Simulation(10000, 0.90, virus, 10)
    sim.logger.write_metadata(10000, 0.90, "Ebola", 0.25, 0.70)
    sim._create_population(10)
    sim.run()
    assert type(sim.logger)==Logger