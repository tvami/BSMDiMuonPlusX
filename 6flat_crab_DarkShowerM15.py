import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'GluGluHToDarkShowers-ScenarioA_ctau-0p1-mA-15-mpi-1_NanoAODScoutingFlat_2024_v3'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cfg_NanoAODScouting_flat_cfg.py'
config.JobType.outputFiles = ['nano_scouting_flat.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.maxMemoryMB = 2500
#config.JobType.numCores = 8

config.section_('Data')
config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/GluGluHToDarkShowers-ScenarioA_ctau-0p1-mA-15-mpi-35_13p6TeV/tvami-crab_GluGluHToDarkShowers-ScenarioA_ctau-0p1-mA-15-mpi-35_MiniAOD_2024_v1-5a58edb2fa3346fa3790a309bf8b307d/USER'
config.Data.outLFNDirBase = '/store/user/tvami/DarkShower/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20 
config.Data.ignoreLocality = True
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
