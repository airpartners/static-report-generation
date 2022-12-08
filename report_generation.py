"""
Author: Andrew DeCandia
Project: Air Partners

Functions to collect figures into a static report PDF
"""
import os, sys
import datetime as dt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from pathlib import Path
from fpdf import FPDF
from PIL import Image
from import_data import DataImporter


def generate_report(month, year, sn):
    generator = ReportGenerator(month, year, sn)
    generator.generate_report()

class ReportGenerator:

    def __init__(self, month, year, sn):
        self.month = month
        self.year = year
        self.sn = sn
        # Convert to date object
        date_obj = dt.date(year, month, 1)
        # format strings for current and previous month
        self.year_month = date_obj.isoformat()[:-3]

    def _create_report_image(self):
        """
        Create JPEG file of static report with compiled visualizations and captions.
        
        :returns: none, makes an image file
        """
        
        def import_and_plot_img(img_path):
            """
            Get PNG files of graphs created for report.

            :param plot_function: string representing function used to create plot.
            :param pm: string with particulate matter for graph, set to None for timeplot
            :returns: none
            """

            plt.grid(0);plt.yticks([]);plt.xticks([])
            img = mpimg.imread(img_path)
            plt.imshow(img)
        
        ################# FIRST PAGE ############################

        fig = plt.figure(figsize=(8.5,11))
        grid = plt.GridSpec(20, 9, wspace=0.3, hspace=10)
        graph_title_position = 0.98
        graph_title_size = 15

        # Subscripts (helpful for captions)
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        
        ## Logos
        fig.add_subplot(grid[:2,:1], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        air_img = plt.imread('_images/airpartners_logo.png', )
        plt.imshow(air_img)

        fig.add_subplot(grid[:2,8:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        ace_img = plt.imread('_images/ace_logo.png')
        plt.imshow(ace_img)
        
        ## Title
        fig.add_subplot(grid[:2,2:7], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        dic_month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        plt.title('Particulate Matter Monthly Summary', fontsize=18, weight='bold', y=0.86)
        plt.suptitle('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=12, y=0.866)
        
        ## Header
        fig.add_subplot(grid[2:6,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0.85, 
            s ='\n\
            This report is a monthly summary of Particulate Matter (PM) data collected as part of the\n\
            community-owned air quality monitoring network jointly managed by Alternatives for Community\n\
            and Environment (ACE) in Roxbury, MA and the Air Partners Group at Olin College of Engineering.\n\
            Data were collected by a QuantAQ Modulair-PM instrument. To learn more, please contact Air Partners\n\
            Research Program Manager Francesca Majluf at fmajluf@olin.edu.\n',
            fontsize=8
        )

        ## Timeplots with Thresholds
        fig.add_subplot(grid[3:9,:], frameon=False)
        plt.title('Particulate Matter Time Series', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img('{1}/Graphs/{2}/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'timeplot_threshold'))
        # Caption
        fig.add_subplot(grid[8:10,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0.15, 
            s='\n\
            Time series for PM1, PM2.5, and PM10 for the entire month. '.translate(SUB)+
            'Upper thresholds represent National Ambient Air Quality\n\
            (NAAQS) 24 h standards, and lower limits represent World Health Organization (WHO) 24 h standards.\n\
            '+
            'No official standards exist for PM1 '.translate(SUB)+
            ', so they are arbitrarily set here at 5 μg/m3 (upper limit) and 2 μg/m3 (lower limit).',
            fontsize=7
        )

        ## Polar plots
        fig.add_subplot(grid[9:16,:3], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm1/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'wind_polar_plot'))

        fig.add_subplot(grid[9:16,3:6], frameon=False)
        plt.title('PM and Wind', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img('{1}/Graphs/{2}/pm25/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'wind_polar_plot'))

        fig.add_subplot(grid[9:16,6:9], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm10/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'wind_polar_plot'))
        # Caption
        fig.add_subplot(grid[15:16,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0, 
            s='\n\
            Polar plots indicate pollutant concentrations as a function of wind speed and wind direction. Pollutant concentrations\n\
            (color scale) are plotted on a compass, with concentric circles representing wind speed (calm at the center, high wind\n\
            speeds on the outside). Warm colors indicate the direction of likely sources of PM relative to the location of the sensor.',
            fontsize=7
        )

        plt.text(
            x=0.3, y=-53,
            s='\n\
            Report continues on next page',
            fontsize=8
        )
        
        # fig.add_subplot(grid[17:20,:], frameon=False)
        # plt.grid(0);plt.yticks([]);plt.xticks([])
        # box_style = dict(boxstyle='round', facecolor='skyblue', alpha=0.5)
        # plt.text(
        #     x=0.07,y=0.5,
        #     s='\n\
        #     Glossary:\n\
        #     PM: Particulate matter (small particles or droplets suspended in the air).                   \n\
        #     {0}: Mass concentration (μg/m3) of particles smaller than 1 μm in diameter.\n\
        #     Sources include fossil fuel combustion.\n\
        #     {1}: Mass concentration (μg/m3) of particles smaller than 2.5 μm in diameter.\n\
        #     Sources include a mixture of fossil fuel combustion and dust sources.\n\
        #     {2}: Mass concentration (μg/m3) of particles smaller than 10 μm in diameter.\n\
        #     Sources include construction, road dust and windblown dust.\n'
        #         .format('PM1'.translate(SUB), 'PM25'.translate(SUB), 'PM10'.translate(SUB)),
        #     fontsize=5, bbox=box_style
        # )

        ## Particle Sizes
        fig.add_subplot(grid[16:20,:6], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        import_and_plot_img('_images/particle_sizes.png')
        
        ## Map
        fig.add_subplot(grid[16:20,6:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        import_and_plot_img('_images/locs/{0}.png'.format(self.sn))


        # Create Pictures directory in Reports directory (if exists, does nothing)
        folders = f'{self.year_month}/Reports/Pictures/{self.sn}'
        Path(folders).mkdir(parents=True, exist_ok=True)
        # Save first page
        plt.savefig('{1}/Reports/Pictures/{0}/{1}_{2}_pg_2.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)
        plt.close()

        ############### SECOND PAGE ####################
        fig2 = plt.figure(figsize=(8.5,11))
        grid2 = plt.GridSpec(20, 9, wspace=0.3, hspace=1)

        ## Logos
        fig2.add_subplot(grid2[:2,:1], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        air_img = plt.imread('_images/airpartners_logo.png', )
        plt.imshow(air_img)

        fig2.add_subplot(grid2[:2,8:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        ace_img = plt.imread('_images/ace_logo.png')
        plt.imshow(ace_img)
        
        ## Title
        fig2.add_subplot(grid2[:2,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title('Particulate Matter Monthly Summary', fontsize=14, weight='bold', y=0.86)
        plt.suptitle('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=10, y=0.866)
        
        ## Calendar plots
        fig2.add_subplot(grid2[1:7,:3], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm1/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'calendar_plot'))

        fig2.add_subplot(grid2[1:7,3:6], frameon=False)
        plt.title('Average (MEAN) Daily PM Concentration', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img('{1}/Graphs/{2}/pm25/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'calendar_plot'))

        fig2.add_subplot(grid2[1:7,6:9], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm10/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'calendar_plot'))

        # Caption
        fig2.add_subplot(grid2[7:8,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=1.5, 
            s='\n\
            Average daily concentration of PM1, PM2.5, and PM10. '.translate(SUB)+ 
            'Dotted lines on the color scale represent NAAQS (upper limit)\n\
            and WHO (lower limit) thresholds for healthy 24 h average PM concentrations. No official standards exist for\n\
            PM1, so they are arbitrarily set here at 5 μg/m3 (upper limit) and 2 μg/m3 (lower limit). No color indicates\n\
            insufficient data to calculate a mean.',
            fontsize=7
        )

        ## Diurnal plots
        fig2.add_subplot(grid2[7:12,:3], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm1/weekday/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'diurnal_plot'))

        fig2.add_subplot(grid2[7:12,3:6], frameon=False)
        plt.title('Daily Trends in PM', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img('{1}/Graphs/{2}/pm25/weekday/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'diurnal_plot'))

        fig2.add_subplot(grid2[7:12,6:9], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm10/weekday/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'diurnal_plot'))

        fig2.add_subplot(grid2[11:16,:3], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm1/weekend/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'diurnal_plot'))

        fig2.add_subplot(grid2[11:16,3:6], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm25/weekend/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'diurnal_plot'))

        fig2.add_subplot(grid2[11:16,6:9], frameon=False)
        import_and_plot_img('{1}/Graphs/{2}/pm10/weekend/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, 'diurnal_plot'))
        # Caption
        fig2.add_subplot(grid2[14:19,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0.45, 
            s='\n\
            These daily average plots (or diurnal profiles) represent a “typical” day in PM trends during the month for\n\
            PM1, PM2.5, and PM10. '.translate(SUB)+
            'Separate plots are made for weekdays and weekends. Lines indicate the median concentrations\n\
            (purple; “what is the amount of PM I am most likely to be exposed to on a typical day?”), and the mean (red;\n\
            “what is the amount of PM I was exposed to on average over the past month?”). Shaded regions represent the\n\
            middle 50% of data (25th-75th percentile) and the middle 90% of data (5th-95th percentile).',
            fontsize=7
        )

        # Save second page
        plt.savefig('{1}/Reports/Pictures/{0}/{1}_{2}_pg_1.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)
        plt.close()


    def _create_report_pdf(self):
        """
        Makes a PDF copy of the jpeg version of the report.
        _create_report_image MUST be run first.
        """
        
        def images_to_pdf(imgs_path, pdf_path):
            # initialize PDF
            pdf = FPDF()
            pdf.set_auto_page_break(0)
            
            img_list = [f'{imgs_path}/{img}' for img in os.listdir(imgs_path)]
            # add pages for each image and place image on page
            for img in img_list:
                # add page with the same size as image
                pdf.add_page()
                pdf.image(img, 0, 8, 210, 280)
                # close the image to save on memory
                Image.open(img).close()
            # save output into assigned PDF path
            pdf.output(pdf_path)
            pdf.close()

        # Create PDFs directory in Reports directory (if exists, does nothing)
        folders = f'{self.year_month}/Reports/PDFs'
        Path(folders).mkdir(parents=True, exist_ok=True)
        # Convert images to PDFs
        images_to_pdf('{1}/Reports/Pictures/{0}'.format(self.sn,self.year_month),
                    '{1}/Reports/PDFs/{0}_{1}_{2}.pdf'.format(self.sn,self.year_month,str('Report')))

    
    def generate_report(self):
        """
        Generate a JPEG and PDF report for a given month and year
        """
        self._create_report_image()
        self._create_report_pdf()


if __name__=='__main__':
    # get year and month from sys args
    year, month = int(sys.argv[1]), int(sys.argv[2])
    # Import sensor data from pickles
    di = DataImporter(year=year, month=month)
    sn_list = di.get_installed_sensor_list()

    # generate reports for each sensor
    for sn in sn_list:
        try:
            generate_report(month, year, sn)
            print(f"Finished report {sn}.")
        except:
            print(f"No report generated {sn}.")
    # generate_report(6, 2022, "MOD-PM-00217")