# static-report-generation

<p float="left">
  <img src="https://github.com/airpartners/static-report-generation/blob/main/_images/example_pg_1.jpeg" alt="Report Example Page 1" width="400"/>
  <img src="https://github.com/airpartners/static-report-generation/blob/main/_images/example_pg_2.jpeg" alt="Report Example Page 2" width="400"/>
</p>

Welcome to the Static Report Generation page! This pipeline creates static reports that summarize the air quality of Roxbury, MA through a sensor network collecting Particulate Matter (PM) data. This sensor network was created and maintained by [Air Partners](https://www.airpartners.org/) in collaboration with [Alternatives for Community and Environment (ACE)](https://ace-ej.org/about/our-team/). The data is collected by [QuantAQ Modulair-PM](https://docs.quant-aq.com/modulair-pm) instruments. 

This service is currently being run on a virtual machine and sends monthly emails to subscribers of an email list with these static reports. To join the mailing list, [subscribe here.](https://forms.gle/1R9e4bzGqPmqYXBP9) For more information on how to read the reports, refer to our file [Report_Reading_Guide.pdf](https://github.com/airpartners/static-report-generation/blob/main/Report_Reading_Guide.pdf) (located at the top level of the repository).

## Running Pipeline Locally

Running the pipeline locally is possible to do to generate your own reports and visualizations so that you can see what the previous month's data looks like without subscribing to the email list. (Please note that there are several files in the repository that will not run due to you not having certain credentials, which means you will not be able to send emails to people on our emailing list, access the Air Partners Dropbox account, or access the sensor deployment logs.)

### Checking System Requirements

After cloning the repo, there are a few steps to running the pipeline. First, make sure you have Python 3.8 or above installed on your computer using your command line.
    
    python -V

This pipeline requires a *ton* of libraries to run properly, which are all listed in `requirements.txt`. If you decide you want to use a virtual environment, [click here](https://pythonbasics.org/virtualenv/) for a basic tutorial on creating and activating it. Regardless, install the necessary libraries needed for the pipeline to work.

    pip install -r requirements.txt
   
### QuantAQ API Key

To download data from our QuantAQ sensors, you must obtain an API key. To do this, go onto [www.quant-aq.com](https://www.quant-aq.com/). Create an account by pressing "Login" on the upper right-hand corner of the screen. Follow the instructions to create an account. 

Once you are logged in, to create an API key, go into your "Console". Under "Console", press "API Keys", and press "Generate New Token" on the upper right-hand corner of your screen. Once you have a token, copy it, go into your command line. Once you are in the `static-report-generation` directory, create a .txt document with your new API key, replacing `<YOUR-API-KEY-HERE>` with your API key that you just created.

    echo "<YOUR-API-KEY-HERE>" > token.txt

### `pipeline.sh`

Once all the libraries are installed, you will need to slightly modify the `pipeline.sh` shell file, since by default it deletes all the visualizations and reports after it is finished running. (This is done since the reports have already been backed up to a Dropbox folder, and the virtual machine on which the service is running has a limited amount of space.) In the shell file, comment out/delete the bottom two lines. 

    #!/bin/sh
    ...
    
    # # delete year-month folder and zip files locally
    # rm -rf $year-$month
    # rm -rf zips/*

Now you can run the pipeline. First, make the pipeline executable.

    chmod u+x pipeline.sh

Then, execute the file.

    ./pipeline.sh
    
If every is working, your computer should start downloading data from the QuantAQ API and should print `Sensor Progress: 1/20`. Unfortunately, the QuantAQ API does take a long time to download data, and it make take up to 15 minutes to download all the data from one sensor. Once the pipeline finishes, you should have a folder containing reports for each sensor, all the graphs for each report, and `.pckl` files containing data from each sensor. 

(Note that some functionality in our pipeline will not be accessible publicly, which may result in some exceptions being thrown. The reports will still render regardless.)


