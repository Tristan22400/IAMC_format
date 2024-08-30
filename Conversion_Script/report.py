def create_report(scenario_df, args):
    # Create instance of FPDF class
    pdf = report_pdf.PDFReport()

    data = scenario_df.filter(
        model=args["model"], scenario=args["scenario"], variable="Primary Energy|*"
    )

    if len(data.variable) > 0:
        data.plot(color="region", title="Primary Energy")
        data.timeseries()
        plt.legend(loc=1)
        plt.tight_layout()
        plt.savefig("Primary_Energy.png")

        # Add a page
        pdf.add_page()
        pdf.ln(50)
        image_path = "Primary_Energy.png"
        page_width = pdf.w
        image_width = 100  # Width of the image
        space_image_text = 10
        x_position = (page_width - image_width) / 2

        # Insert image
        pdf.image(image_path, x=x_position, y=40, w=image_width)

        # Insert text centered just below the image
        pdf.ln(image_width)  # Move down by the height of the image
        pdf.set_y(space_image_text + image_width)  # Ensure the text is below the image

        # Calculate text width and center
        text = "Figure 1: World Primary Energy Consumption"
        text_width = pdf.get_string_width(text)
        pdf.set_x((page_width - text_width) / 2)  # Center the text

        # Insert text
        pdf.cell(text_width, 10, txt=text, ln=2, border=0, align="C")

        # Center the second image
        second_image_path = "Primary_Energy.png"
        second_image_y = (
            image_width + 4 * space_image_text
        )  # Adjust y to place the second image below the text

        # Insert the second image
        pdf.image(second_image_path, x=x_position, y=second_image_y, w=image_width)

        # Insert text centered just below the image
        pdf.ln(image_width)  # Move down by the height of the image
        pdf.set_y(
            2 * image_width + space_image_text
        )  # Ensure the text is below the image

        # Calculate text width and center
        text = "Figure 1: World Primary Energy Consumption"
        text_width = pdf.get_string_width(text)
        pdf.set_x((page_width - text_width) / 2)  # Center the text

        # Insert text
        pdf.cell(text_width, 10, txt=text, ln=2, border=0, align="C")

        pdf.output(args["scenario"] + "report.pdf", "F")
