import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'QCD_Bin-PT-15to20_NanoAODScoutingFlat_2024_v1'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'NanoAODScouting-01654_1_flat_cfg.py'
config.JobType.outputFiles = ['Summer24NanoAODv15-01654_scouting_flat.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.maxMemoryMB = 2500
#config.JobType.numCores = 8

config.section_('Data')
#config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/QCD_Bin-PT-15to20_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/RunIII2024Summer24MiniAODv6-150X_mcRun3_2024_realistic_v2-v2/MINIAODSIM'
config.Data.outLFNDirBase = '/store/user/tvami/DiMuonPlusX/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20 
config.Data.ignoreLocality = True
config.Data.publication = True
config.Data.allowNonValidInputDataset = True


config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
