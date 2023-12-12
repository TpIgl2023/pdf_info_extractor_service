import logging

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

from dotenv import *

from Services.FileHandler import FileHandler

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class AdobeServicesHandler:
    def __init__(self):
        pass

    @staticmethod
    def process(pdf_path):
        # Initial setup, create credentials instance.
        credentials = Credentials.service_principal_credentials_builder(). \
            with_client_id(CLIENT_ID). \
            with_client_secret(CLIENT_SECRET). \
            build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(pdf_path)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(ZIP_PATH)

    @staticmethod
    def extractText(pdf_path):
        try:
            AdobeServicesHandler.process(pdf_path)
            # Unzip and remove the zipped file
            FileHandler.unzip(ZIP_PATH, UNZIP_PATH)
            os.remove(ZIP_PATH)

            # Extract the structured data from the Json file
            text = ""
            try:
                text = FileHandler.loadText(STRUCTURED_DATA_PATH)
            except:
                pass
            return text
        except (ServiceApiException, ServiceUsageException, SdkException):
            logging.exception("Exception encountered while executing operation")
