"""
Author: Andrew DeCandia
Project: Air Partners

Functions to collect figures into a static report PDF
"""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from pathlib import Path
import img2pdf
import os


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

        fig = plt.figure(figsize=(8.3,11.7))
        grid = plt.GridSpec(20, 9, wspace=0.3, hspace=10)
        graph_title_position = 0.98
        graph_title_size = 15

        ## Header
        fig.add_subplot(grid[:4,:6], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
        'This report has data collected from the community owned air sensor network in Roxbury in collaboration\n\
        with ACE. The sensors are QuantAQ ModulairTM PM and measure Particulate Matter (PM) from burning fossil\n\
        fuels that is harmful to human health. If you have any questions or concerns, please contact\n\
        <INSERT CONTACT INFO>.'
            ,fontsize=8, y=0.1)
        dic_month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        plt.suptitle('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=21, y=0.86)

        ## Glossary
        fig.add_subplot(grid[:4,7:9])
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'Glossary: \n\
            Term 1: definition\n\
            Term 2: definition\n\
            Term 3: definition\n\
            \tSubpoint\n\
            \tSubpoint',
            fontsize=6, y=0.1
        )

        ## Timeplots with Thresholds
        fig.add_subplot(grid[4:10,:], frameon=False)
        plt.title('PM Over Time', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("timeplot_threshold")
        # Caption
        fig.add_subplot(grid[10:12,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'This timeplot shows the levels of PM of different diameters (<10μm, <2.5μm, and <1μm, respectively)\n\
            over the course of the month. The different colors represent different thresholds based on national\n\
            standards of air quality and WHO (World Health Organization) air quality guidelines. The thresholds\n\
            defined for PM2.5 are used for the other color scales on the calendar plot and the wind polar plot. (See below.)',
            fontsize=6, y=0.1
        )

        ## Calendar plots
        fig.add_subplot(grid[12:18,:3], frameon=False)
        plt.title(r'$PM_1$ Calendar', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("calendar_plot", "pm1")

        fig.add_subplot(grid[12:18,3:6], frameon=False)
        plt.title(r'$PM_{2.5}$ Calendar', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("calendar_plot", "pm25")

        fig.add_subplot(grid[12:18,6:9], frameon=False)
        plt.title(r'$PM_{10}$ Calendar', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("calendar_plot", "pm10")

        # Caption
        fig.add_subplot(grid[18:20,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'This is a calendar which shows the daily average (median?) concentration of PM2.5 over the month. The\n\
            color scale takes into account the WHO and EPA air quality standards of 5 μg/m³ and 12 μg/m³, respectively.',
            fontsize=6, y=0.1
        )

        # Create Pictures directory in Reports directory (if exists, does nothing)
        folders = f'{self.year_month}/Reports/Pictures'
        Path(folders).mkdir(parents=True, exist_ok=True)
        # Save first page
        plt.savefig('{1}/Reports/Pictures/{0}_{1}_{2}_pg_1.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)

        ############### SECOND PAGE ####################
        fig2 = plt.figure(figsize=(8.3,11.7))
        grid2 = plt.GridSpec(20, 9, wspace=0.3, hspace=10)
        
        ## Header (same as before)
        fig2.add_subplot(grid2[:4,:6], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
        'This report has data collected from the community owned air sensor network in Roxbury in collaboration\n\
        with ACE. The sensors are QuantAQ ModulairTM PM and measure Particulate Matter (PM) from burning fossil\n\
        fuels that is harmful to human health. If you have any questions or concerns, please contact\n\
        <INSERT CONTACT INFO>.'
            ,fontsize=8, y=0.1)
        dic_month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        plt.suptitle('  {0} {1}: {2}'.format(dic_month[self.month], self.year, self.sn), fontsize=21, y=0.86)

        ## Glossary
        fig2.add_subplot(grid2[:4,7:9])
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'Glossary: \n\
            Term 1: definition\n\
            Term 2: definition\n\
            Term 3: definition\n\
            \tSubpoint\n\
            \tSubpoint',
            fontsize=6, y=0.1
        )
        
        ## Polar plots
        fig2.add_subplot(grid2[4:10,:3], frameon=False)
        plt.title(r'Polar Plot $PM_1$', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("wind_polar_plot", "pm1")

        fig2.add_subplot(grid2[4:10,3:6], frameon=False)
        plt.title(r'Polar Plot $PM_{2.5}$', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("wind_polar_plot", "pm25")

        fig2.add_subplot(grid2[4:10,6:9], frameon=False)
        plt.title(r'Polar Plot $PM_{10}$', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("wind_polar_plot", "pm10")
        # Caption
        fig2.add_subplot(grid2[10:12,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'The above polar plot shows concentrations of PM2.5 based on wind data. Yellow and red colors indicate\n\
            where concentrations of PM2.5 are higher relative to the location of the sensor.',
            fontsize=6, y=0.1
        )

        ## Diurnal plots
        fig2.add_subplot(grid2[12:18,:3], frameon=False)
        plt.title(r'Diurnal Plot $PM_1$', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("diurnal_plot", "pm1")

        fig2.add_subplot(grid2[12:18,3:6], frameon=False)
        plt.title(r'Diurnal Plot $PM_{2.5}$', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("diurnal_plot", "pm25")

        fig2.add_subplot(grid2[12:18,6:9], frameon=False)
        plt.title(r'Diurnal Plot $PM_{10}$', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("diurnal_plot", "pm10")
        # Caption
        fig2.add_subplot(grid2[18:20,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'The above plots show various metrics about the air quality by this sensor on a given day.\n\
            (Add more text about those metrics here.)',
            fontsize=6, y=0.1
        )

        # Save second page
        plt.savefig('{1}/Reports/Pictures/{0}_{1}_{2}_pg_2.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)


    def _create_report_pdf(self):
        """
        Makes a PDF copy of the jpeg version of the report.
        _create_report_image MUST be run first.
        """

        # Function to convert image into PDF
        def image_to_pdf(img_path, pdf_path):
            ImgFile = open(img_path,"rb")
            PdfFile = open(pdf_path,"wb")
            PdfFile.write(img2pdf.convert(ImgFile))
            ImgFile.close()
            PdfFile.close()

        # Create PDFs directory in Reports directory (if exists, does nothing)
        folders = f'{self.year_month}/Reports/PDFs'
        Path(folders).mkdir(parents=True, exist_ok=True)
        # Convert images to PDFs
        image_to_pdf('{1}/Reports/Pictures/{0}_{1}_{2}.jpeg'.format(self.sn,self.year_month,str('Report')),
                    '{1}/Reports/PDFs/{0}_{1}_{2}.pdf'.format(self.sn,self.year_month,str('Report')))

    
    def generate_report(self):
        """
        Generate a JPEG and PDF report for a given month and year
        """
        self._create_report_image()
        self._create_report_pdf()


if __name__=='__main__':
    generate_report(4, 2022, 'MOD-PM-00218')
