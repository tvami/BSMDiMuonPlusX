import os
import glob

from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'gg2H_H2A_MuMuBB-mA3-15-mH1-125-mH2-100_NanoGen_2024_v2'

config.section_('JobType')
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cfg_nanogen_only.py'
config.JobType.outputFiles = ['NanoGen.root']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.maxMemoryMB = 2500
#config.JobType.numCores = 8

config.section_('Data')
config.Data.inputDBS = 'phys03'
config.Data.inputDataset = '/gg2H_H2A_MuMuBB-mA3-15-mH1-125-mH2-100_13p6TeV/tvami-gg2H_H2A_MuMuBB-mA3-15-mH1-125-mH2-100_GENSIM_2024_v2-5beaa20e1f8d710506130f12fa51c293/USER'
config.Data.outLFNDirBase = '/store/user/tvami/DarkShower/'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50
#config.Data.totalUnits = 1
config.Data.ignoreLocality = True
config.Data.publication = True

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_DE_DESY','T2_CH_CERN','T2_IT_Bari','T1_IT_*','T2_US_*', 'T3_US_FNALLPC','T2_HU_Budapest','T2_FR_*', 'T2_UK_London_IC']
