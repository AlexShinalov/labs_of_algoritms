import pandas

import jpype
from jpype import JPackage
jpype.startJVM()
import arx
##, usecols=['Название магазина', 'Координаты  и время', 'Категория', 'Бренд', 'Номер карты', 'Кол-во', 'Цена']

#excel_data_df = pandas.read_excel('output.xlsx', sheet_name='Sheet1')
#excel_data_df.to_csv('data.csv')

ARX = jpype.JPackage('arx')
ARXConfiguration = ARX.deidentifier.ARXConfiguration
ARXData = ARX.deidentifier.ARXData
ARXConfigurationFile = ARX.deidentifier.config.ARXConfigurationFile
ARXMasking = ARX.deidentifier.masks.ARXMasking
ARXPerturbation = ARX.deidentifier.perturb.ARXPerturbation

def mask_perturb_with_arx(input_file, config_file, output_file):
    # Create configuration
    config = ARXConfiguration.create()

    # Load ARX configuration file
    configFile = ARXConfigurationFile.create()
    configFile.setFile(config_file)
    config.addPrivacyModel(configFile.load())

    # Load data
    data = ARXData.create()
    data.loadCSVFile(input_file)
    dataset = data.getHandle().getDataset()

    # Masking
    mask = ARXMasking.create()
    result_masked = mask.anonymize(dataset, config)

    # Perturbation
    perturb = ARXPerturbation.create()
    result_perturbed = perturb.anonymize(result_masked, config)

    # Save anonymized data
    data.getHandle().save(result_perturbed, output_file)

# Example usage
mask_perturb_with_arx('input.csv', 'config.xml', 'output.csv')

# Shutdown the JVM when done
jpype.shutdownJVM()


