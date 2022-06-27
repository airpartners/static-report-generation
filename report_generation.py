"""
Author: Andrew DeCandia
Project: Air Partners

Functions to collect figures into a static report PDF
"""
import os, sys
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
        self.year_month = str(self.year) + '-0' + str(self.month) if self.month <= 9 else str(self.year) + '-' + str(self.month)

    def _create_report_image(self):
        """
        Create JPEG file of static report with compiled visualizations and captions.
        """

        def import_and_plot_img(plot_function, pm):
            """
            Get PNG files of graphs created for report.

            Args:
                plot_function: string representing function used to create plot.
                pm: string with particulate matter for graph, set to None for timeplot
            Returns:
                None
            """

            plt.grid(0);plt.yticks([]);plt.xticks([])
            if pm==None:
                img = mpimg.imread('{1}/Graphs/{2}/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, plot_function))
            else:
                img = mpimg.imread('{1}/Graphs/{2}/{3}/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, plot_function, pm))
            plt.imshow(img)
        
        ################# FIRST PAGE ############################

        fig = plt.figure(figsize=(8.5,11))
        grid = plt.GridSpec(20, 9, wspace=0.3, hspace=10)
        graph_title_position = 0.98
        graph_title_size = 15

        ## Title
        fig.add_subplot(grid[:2,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        dic_month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        plt.title('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=21, y=0.86)
        
        ## Header
        fig.add_subplot(grid[2:6,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0, 
            s ='\n\
            This report has data collected from the community owned air sensor network in\n\
            Roxbury in collaboration with ACE. The sensors are QuantAQ ModulairTM PM and\n\
            measure Particulate Matter (PM) from burning fossil fuels that is harmful to\n\
            human health. If you have any questions or concerns, please contact\n\
            <INSERT CONTACT INFO>.\n\n\
            Glossary: \n\
            Term 1: definition\n\
            Term 2: definition\n\
            Term 3: definition\n\
            \tSubpoint\n\
            \tSubpoint'
        )

        ## Timeplots with Thresholds
        fig.add_subplot(grid[6:12,:], frameon=False)
        plt.title('PM Over Time', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("timeplot_threshold", pm=None)
        # Caption
        fig.add_subplot(grid[12:13,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=-5, 
            s='\n\
            This timeplot shows the levels of PM of different diameters (<10μm, <2.5μm, and <1μm, respectively)\n\
            over the course of the month. The different colors represent different thresholds based on national\n\
            standards of air quality and WHO (World Health Organization) air quality guidelines. The thresholds\n\
            defined for PM2.5 are used for the other color scales on the calendar plot and the wind polar plot.\n\
            (See next page.)',
            fontsize=8
        )

        ## Calendar plots
        fig.add_subplot(grid[13:19,:3], frameon=False)
        import_and_plot_img("calendar_plot", "pm1")

        fig.add_subplot(grid[13:19,3:6], frameon=False)
        plt.title('PM Concentration Calendars', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("calendar_plot", "pm25")

        fig.add_subplot(grid[13:19,6:9], frameon=False)
        import_and_plot_img("calendar_plot", "pm10")

        # Caption
        fig.add_subplot(grid[19:20,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0, 
            s='\n\
            These calendars show the daily average concentration of $PM_1$, $PM_{2.5}$, and $PM_{10}$ over the month.\n\
            The color scale takes into account the WHO and EPA air quality standards of 5 μg/m³ and 12 μg/m³,\n\
            respectively.',
            fontsize=8
        )

        # Create Pictures directory in Reports directory (if exists, does nothing)
        folders = f'{self.year_month}/Reports/Pictures/{self.sn}'
        Path(folders).mkdir(parents=True, exist_ok=True)
        # Save first page
        plt.savefig('{1}/Reports/Pictures/{0}/{1}_{2}_pg_2.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)
        plt.close()

        ############### SECOND PAGE ####################
        fig2 = plt.figure(figsize=(8.5,11))
        grid2 = plt.GridSpec(20, 9, wspace=0.3, hspace=10)
        graph_title_position = 0.98
        graph_title_size = 15

        ## Title
        fig2.add_subplot(grid[:2,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=21, y=0.86)
        
        ## Header
        fig2.add_subplot(grid2[2:6,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0, 
            s ='\n\
            This report has data collected from the community owned air sensor network in\n\
            Roxbury in collaboration with ACE. The sensors are QuantAQ ModulairTM PM and\n\
            measure Particulate Matter (PM) from burning fossil fuels that is harmful to\n\
            human health. If you have any questions or concerns, please contact\n\
            <INSERT CONTACT INFO>.\n\n\
            Glossary: \n\
            Term 1: definition\n\
            Term 2: definition\n\
            Term 3: definition\n\
            \tSubpoint\n\
            \tSubpoint'
        )
        
        ## Polar plots
        fig2.add_subplot(grid2[6:12,:3], frameon=False)
        import_and_plot_img("wind_polar_plot", "pm1")

        fig2.add_subplot(grid2[6:12,3:6], frameon=False)
        plt.title('PM Wind Polar Plots', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("wind_polar_plot", "pm25")

        fig2.add_subplot(grid2[6:12,6:9], frameon=False)
        import_and_plot_img("wind_polar_plot", "pm10")
        # Caption
        fig2.add_subplot(grid2[12:13,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0, 
            s='\n\
            The above polar plots show concentrations of different PMs based on wind data. Yellow and red colors indicate\n\
            where concentrations of $PM_1$, $PM_{2.5}$, and $PM_{10}$ are higher relative to the location of the sensor.',
            fontsize=8
        )

        ## Diurnal plots
        fig2.add_subplot(grid2[13:19,:3], frameon=False)
        import_and_plot_img("diurnal_plot", "pm1")

        fig2.add_subplot(grid2[13:19,3:6], frameon=False)
        plt.title('PM Diurnal Plots', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("diurnal_plot", "pm25")

        fig2.add_subplot(grid2[13:19,6:9], frameon=False)
        import_and_plot_img("diurnal_plot", "pm10")
        # Caption
        fig2.add_subplot(grid2[19:20,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.text(
            x=0, y=0, 
            s='\n\
            The above plots show various metrics about the air quality by this sensor on a given day.\n\
            (Add more text about those metrics here.)',
            fontsize=8
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
    sn_list, sn_dict = di.get_PM_data()

    # generate reports for each sensor
    for sn in sn_list:
        if not sn_dict[sn].empty:
            generate_report(month, year, sn)
            print(f"Finished report {sn}.")