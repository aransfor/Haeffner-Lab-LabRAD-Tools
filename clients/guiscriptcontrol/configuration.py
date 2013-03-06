class config(object):
    
    
    #dictionary in the form semaphore_path: (import_part, name)
    ExperimentInfo = {
     ('Test', 'Exp1'):  ('common.clients.guiscriptcontrol.experiments.Test', 'Test'),
     ('729Experiments','Spectrum'):  ('cct.scripts.experiments.Experiments729.spectrum', 'spectrum'),
     ('729Experiments','RabiFlopping'):  ('cct.scripts.experiments.Experiments729.rabi_flopping', 'rabi_flopping'),
     ('shuttling', 'shuttle'): ('cct.scripts.experiments.Experiments729.shuttle', 'shuttle'),
     }
    
    
    #conflicting experiments, every experiment conflicts with itself
    conflictingExperiments = {    
    ('Test', 'Exp1'): [('Test', 'Exp1')],
    ('729Experiments','Spectrum'):  [('729Experiments','Spectrum')],
    ('729Experiments','RabiFlopping'):  [('729Experiments','RabiFlopping')],
    ('shuttling', 'shuttle'): [('shuttling', 'shuttle')],
    }