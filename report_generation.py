"""
Author: Andrew DeCandia
Project: Air Partners

Functions to collect figures into a static report PDF
"""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
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

        def import_and_plot_img(plot_function):
            """
            Get PNG files of graphs created for report.

            Args:
                plot_function: string representing function used to create plot.
            Returns:
                None
            """

            plt.grid(0);plt.yticks([]);plt.xticks([])
            img = mpimg.imread('{1}/Graphs/{2}/{0}_{1}_{2}.jpeg'.format(self.sn, self.year_month, plot_function))
            plt.imshow(img)
        
        # Create initial figure (report)
        fig = plt.figure(figsize=(8.3,11.7))
        grid = plt.GridSpec(23, 6, wspace=0.3, hspace=10)
        graph_title_position = 0.98
        graph_title_size = 15

        ## Header
        fig.add_subplot(grid[:4,:], frameon=False)
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

        ## Timeplots with Thresholds
        fig.add_subplot(grid[4:10,:], frameon=False)
        plt.title('PM Over Time', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("timeplot_threshold")
        # Caption
        fig.add_subplot(grid[10:11,:], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'This timeplot shows the levels of PM of different diameters (<10μm, <2.5μm, and <1μm, respectively)\n\
            over the course of the month. The different colors represent different thresholds based on national\n\
            standards of air quality and WHO (World Health Organization) air quality guidelines. The thresholds\n\
            defined for PM2.5 are used for the other color scales on the calendar plot and the wind polar plot. (See below.)',
            fontsize=6, y=0.1
        )

        ## Calendar plot
        fig.add_subplot(grid[11:16,:3], frameon=False)
        plt.title('Calendar', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("calendar_plot")
        # Caption
        fig.add_subplot(grid[16:17,:3], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'This is a calendar which shows the daily average (median?)\n\
            concentration of PM2.5 over the month. The color scale\n\
            takes into account the WHO and EPA air quality standards\n\
            of 5 μg/m³ and 12 μg/m³, respectively.',
            fontsize=6, y=0.1
        )

        ## Time of day plot
        fig.add_subplot(grid[11:16,3:6], frameon=False)
        plt.title('Time of Day', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("time_of_day_plot")
        # Caption
        fig.add_subplot(grid[16:17,3:6], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'The figure above shows the average levels of PM1, PM2.5, and PM10\n\
            over the course of the average day.',
            fontsize=6, y=0.1
        )

        ## Daily average plot
        fig.add_subplot(grid[17:22,:3], frameon=False)
        plt.title('Daily Average', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("daily_average_plot")
        # Caption
        fig.add_subplot(grid[22:23,:3], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'This figure shows the average levels of PM1, PM2.5, and PM10 for each\n\
            day over the course of the month. Note that the calendar plot displays\n\
            the same for only PM2.5.',
            fontsize=6, y=0.1
        )

        ## Polar plot
        fig.add_subplot(grid[17:22,3:6], frameon=False)
        plt.title('Polar Plot', y=graph_title_position,fontsize=graph_title_size)
        import_and_plot_img("wind_polar_plot")
        # Caption
        fig.add_subplot(grid[22:23,3:6], frameon=False)
        plt.grid(0);plt.yticks([]);plt.xticks([])
        plt.title(
            'The above polar plot shows concentrations of PM2.5 based on wind data.\n\
            Yellow and red colors indicate where concentrations of PM2.5 are higher\n\
            relative to the location of the sensor.',
            fontsize=6, y=0.1
        )

        # Save newly created reports to Reports directory
        try:
            os.mkdir('{}/Reports'.format(self.year_month))
        except: # Forgive my crime here, but it just avoids errors if the directory already exists
            pass
        plt.savefig('{1}/Reports/{0}_{1}_{2}.jpeg'.format(self.sn,self.year_month,str('Report')), bbox_inches='tight',dpi = 300)

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

        # Create and save newly created PDF reports to Reports directory
        try:
            os.mkdir('{}/Reports/PDFs'.format(self.year_month))
        except: # Forgive my crime here, but it just avoids errors if the directory already exists
            pass
        image_to_pdf('{1}/Reports/{0}_{1}_{2}.jpeg'.format(self.sn,self.year_month,str('Report')),
                    '{1}/Reports/PDFs/{0}_{1}_{2}.pdf'.format(self.sn,self.year_month,str('Report')))

    
    def generate_report(self):
        """
        Generate a JPEG and PDF report for a given month and year
        """
        self._create_report_image()
        self._create_report_pdf()


if __name__=='__main__':
    generate_report(4, 2022, 'MOD-PM-00218')
