import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'GluGluHToDarkShowers-ScenarioA_ctau-15-mA-0p25-mpi-35_AOD_2024_v1'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'EXO-RunIII2024Summer24DRPremix-01654_2_cfg.py'
config.JobType.outputFiles = ['EXO-RunIII2024Summer24DRPremix-01654.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.maxMemoryMB = 4000
#config.JobType.numCores = 8

config.section_('Data')
config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/GluGluHToDarkShowers-ScenarioA_ctau-0p1-mA-15-mpi-35_13p6TeV/tvami-crab_GluGluHToDarkShowers-ScenarioA_ctau-0p1-mA-15-mpi-35_DR_2024_v1-abf5c6478764194191930dea949a157a/USER'
config.Data.outLFNDirBase = '/store/user/tvami/DarkShower/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.ignoreLocality = True
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
