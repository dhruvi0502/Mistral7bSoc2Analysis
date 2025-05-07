from flask import request, Flask, jsonify, abort
import os
import requests
import Mistral7BHuggingFaceTable as SOCAnalysis
import time
from flask_cors import CORS
#Create the Flask Application Object 

app = Flask(__name__)
CORS(app, resources={r"/SOC2Analysis": {"origins": "http://localhost:3000"}})


#define the route and the function
@app.route('/SOC2Analysis', methods = ['POST'])
def selectFileAndAnalysis():
    pdfFileURL = request.json['PDFFileURL']
    analysisType = request.json['AnalysisType']
    if not pdfFileURL:
        return jsonify(
            {
                "Status_Code" : 404,
                "Message" : "FilePath Is Missing."
            }
        )#abort(404, description="FilePath Is Missing.")
    sTR = time.time()
    response = requests.get(pdfFileURL, stream=True)
    print("End Time Request: " , time.time() - sTR)
    try:
        if response.status_code != 200:
            return jsonify(
                {
                    "Status_Code" : 404,
                    "Message" : "File could not be downloaded from the URL."
                }
            )#abort(404, description="File could not be downloaded from the URL.")
        
        # Infer filename from URL or default
        sTD = time.time()
        filename = pdfFileURL.split("/")[-1].split("?")[0]
        if not filename.lower().endswith('.pdf'):
            filename += ".pdf"
        print(filename)
        currentWorkingDir = os.getcwd()
        print(currentWorkingDir)
        downloadFolderPath = os.path.join(currentWorkingDir,"Download")
        print("Folder Name : ", downloadFolderPath)
        pdfFilePath = os.path.join(downloadFolderPath,filename)
        print("path : " ,pdfFilePath)
        if os.path.exists(pdfFilePath):
            os.remove(pdfFilePath)
        with open(pdfFilePath,'wb') as filewrite:
            filewrite.write(response.content)
        print("End Time Save PDf : " , time.time() - sTD)
        
    except Exception as e:
        description=f"Error downloading file: {str(e)}"
        return jsonify(
            {
                "Status_Code" : 500,
                "Message" : description
            }
        )#abort(500, description=f"Error downloading file: {str(e)}")
    #pdfFilePath = "D:/1_Job _AI-ML/SOC2ReportAnalysisCode/Download/680b7dfa791417f2de22faee.pdf"
    #analysisType = "all"
    sTM = time.time()
    modelResponse = SOCAnalysis.AnalysisOfSoc2Report(analysisType, pdfFilePath)
    print("Full time taken for model Response : " , time.time() - sTM)
    os.remove(pdfFilePath)
    if modelResponse is None:
         return jsonify(
             {
                 "Status_Code" : 404,
                 "Message" : "Not a Soc2 Report file.."
             }
         )#abort(404, description="Not a Soc2 Report file..")
    
    print("Send Response : ", modelResponse)
    match analysisType:
        case "all":
            return jsonify(
                {
                    "Status_Code" : 200,
                    "Message" : "Analysis Result..",
                    "Security" : modelResponse["security Score"],
                    "S_High Risk" : modelResponse["S_High Risk Score"],
                    "S_Medium Risk" : modelResponse["S_Medium Risk Score"] ,
                    "S_Low Risk" : modelResponse["S_Low Risk Score"],
                    "S_AI-Powered Actions" : modelResponse["S_AI-Powered Actions Score"],
                    "S_Informative" : modelResponse["S_Informative Score"],
                    "SCaption" : modelResponse["SCaption"],
                    "Availability" : modelResponse["availability Score"],
                    "A_High Risk" : modelResponse["A_High Risk Score"] ,
                    "A_Medium Risk" : modelResponse["A_Medium Risk Score"] ,
                    "A_Low Risk" : modelResponse["A_Low Risk Score"],
                    "A_AI-Powered Actions" : modelResponse["A_AI-Powered Actions Score"],
                    "A_Informative" : modelResponse["A_Informative Score"],
                    "ACaption" : modelResponse["ACaption"],                    
                    "Confidentiality" : modelResponse["confidentiality Score"],
                    "C_High Risk" : modelResponse["C_High Risk Score"] ,
                    "C_Medium Risk" : modelResponse["C_Medium Risk Score"] ,
                    "C_Low Risk" : modelResponse["C_Low Risk Score"],
                    "C_AI-Powered Actions" : modelResponse["C_AI-Powered Actions Score"],
                    "C_Informative" : modelResponse["C_Informative Score"],
                    "CCaption" : modelResponse["CCaption"], 
                    "ProcessingIntegrity" : modelResponse["processingIntegrity Score"],
                    "PI_High Risk" : modelResponse["PI_High Risk Score"] ,
                    "PI_Medium Risk" : modelResponse["PI_Medium Risk Score"] ,
                    "PI_Low Risk" : modelResponse["PI_Low Risk Score"],
                    "PI_AI-Powered Actions" : modelResponse["PI_AI-Powered Actions Score"],
                    "PI_Informative" : modelResponse["PI_Informative Score"],
                    "PICaption" : modelResponse["PICaption"],
                    "Privacy" : modelResponse["privacy Score"],
                    "P_Data Leak Alerts" : modelResponse["P_Data Leak Alerts Score"],
                    "P_Conset Monitoring" : modelResponse["P_Conset Monitoring Score"],
                    "P_Encryption Enforcement" : modelResponse["P_Encryption Enforcement Score"],
                    "P_Audit Trail Tracking" : modelResponse["P_Audit Trail Tracking Score"],
                    "P_Informative" : modelResponse["P_Informative Score"],
                    "PCaption" : modelResponse["PCaption"]

                }
            )
        case "security":
            return jsonify(
                {
                    "Status_Code" : 200,
                    "Message" : "Analysis Result..",
                    "Security" : modelResponse["security Score"],
                    "S_High Risk" : modelResponse["S_High Risk Score"],
                    "S_Medium Risk" : modelResponse["S_Medium Risk Score"] ,
                    "S_Low Risk" : modelResponse["S_Low Risk Score"],
                    "S_AI-Powered Actions" : modelResponse["S_AI-Powered Actions Score"],
                    "S_Informative" : modelResponse["S_Informative Score"],
                    "SCaption" : modelResponse["SCaption"],
                    "Availability" : 0,
                    "A_High Risk" : 0 ,
                    "A_Medium Risk" : 0 ,
                    "A_Low Risk" : 0,
                    "A_AI-Powered Actions" : 0,
                    "A_Informative" : 0,
                    "ACaption" : "No Data",                    
                    "Confidentiality" : 0,
                    "C_High Risk" : 0 ,
                    "C_Medium Risk" : 0 ,
                    "C_Low Risk" : 0,
                    "C_AI-Powered Actions" : 0,
                    "C_Informative" : 0,
                    "CCaption" : "No Data", 
                    "ProcessingIntegrity" : 0,
                    "PI_High Risk" : 0 ,
                    "PI_Medium Risk" : 0 ,
                    "PI_Low Risk" : 0,
                    "PI_AI-Powered Actions" : 0,
                    "PI_Informative" : 0,
                    "PICaption" : "No Data",
                    "Privacy" : 0,
                    "P_Data Leak Alerts" : 0,
                    "P_Conset Monitoring" : 0,
                    "P_Encryption Enforcement" : 0,
                    "P_Audit Trail Tracking" : 0,
                    "P_Informative" : 0,
                    "PCaption" : "No Data"
                }                
            )
        case "availability":
            return jsonify(
                {
                    "Status_Code" : 200,
                    "Message" : "Analysis Result..",
                    "Security" : 0,
                    "S_High Risk" : 0,
                    "S_Medium Risk" : 0,
                    "S_Low Risk" : 0,
                    "S_AI-Powered Actions" : 0,
                    "S_Informative" : 0,
                    "SCaption" : "No Data",
                    "Availability" : modelResponse["availability Score"],
                    "A_High Risk" : modelResponse["A_High Risk Score"] ,
                    "A_Medium Risk" : modelResponse["A_Medium Risk Score"] ,
                    "A_Low Risk" : modelResponse["A_Low Risk Score"],
                    "A_AI-Powered Actions" : modelResponse["A_AI-Powered Actions Score"],
                    "A_Informative" : modelResponse["A_Informative Score"],
                    "ACaption" : modelResponse["ACaption"],                    
                    "Confidentiality" : 0,
                    "C_High Risk" : 0 ,
                    "C_Medium Risk" : 0 ,
                    "C_Low Risk" : 0,
                    "C_AI-Powered Actions" : 0,
                    "C_Informative" : 0,
                    "CCaption" : "No Data", 
                    "ProcessingIntegrity" : 0,
                    "PI_High Risk" : 0 ,
                    "PI_Medium Risk" : 0 ,
                    "PI_Low Risk" : 0,
                    "PI_AI-Powered Actions" : 0,
                    "PI_Informative" : 0,
                    "PICaption" : "No Data",
                    "Privacy" : 0,
                    "P_Data Leak Alerts" : 0,
                    "P_Conset Monitoring" : 0,
                    "P_Encryption Enforcement" : 0,
                    "P_Audit Trail Tracking" : 0,
                    "P_Informative" : 0,
                    "PCaption" : "No Data"
                }
            )
        case "confidentiality":
            return jsonify(
                {
                    "Status_Code" : 200,
                    "Message" : "Analysis Result..",
                    "Security" : 0,
                    "S_High Risk" : 0,
                    "S_Medium Risk" : 0,
                    "S_Low Risk" : 0,
                    "S_AI-Powered Actions" : 0,
                    "S_Informative" : 0,
                    "SCaption" : "No Data",
                    "Availability" : 0,
                    "A_High Risk" : 0 ,
                    "A_Medium Risk" : 0 ,
                    "A_Low Risk" : 0,
                    "A_AI-Powered Actions" : 0,
                    "A_Informative" : 0,
                    "ACaption" : "No Data",                    
                    "Confidentiality" : modelResponse["confidentiality Score"],
                    "C_High Risk" : modelResponse["C_High Risk Score"] ,
                    "C_Medium Risk" : modelResponse["C_Medium Risk Score"] ,
                    "C_Low Risk" : modelResponse["C_Low Risk Score"],
                    "C_AI-Powered Actions" : modelResponse["C_AI-Powered Actions Score"],
                    "C_Informative" : modelResponse["C_Informative Score"],
                    "CCaption" : modelResponse["CCaption"], 
                    "ProcessingIntegrity" : 0,
                    "PI_High Risk" : 0 ,
                    "PI_Medium Risk" : 0 ,
                    "PI_Low Risk" : 0,
                    "PI_AI-Powered Actions" : 0,
                    "PI_Informative" : 0,
                    "PICaption" : "No Data",
                    "Privacy" : 0,
                    "P_Data Leak Alerts" : 0,
                    "P_Conset Monitoring" : 0,
                    "P_Encryption Enforcement" : 0,
                    "P_Audit Trail Tracking" : 0,
                    "P_Informative" : 0,
                    "PCaption" : "No Data"
                }
            )
        
        case "processingIntegrity":
            return jsonify(
                {
                    "Status_Code" : 200,
                    "Message" : "Analysis Result..",
                    "Security" : 0,
                    "S_High Risk" : 0,
                    "S_Medium Risk" : 0,
                    "S_Low Risk" : 0,
                    "S_AI-Powered Actions" : 0,
                    "S_Informative" : 0,
                    "SCaption" : "No Data",
                    "Availability" : 0,
                    "A_High Risk" : 0,
                    "A_Medium Risk" : 0,
                    "A_Low Risk" : 0,
                    "A_AI-Powered Actions" : 0,
                    "A_Informative" : 0,
                    "ACaption" : "No Data",                    
                    "Confidentiality" : 0,
                    "C_Heigh Risk" : 0 ,
                    "C_Medium Risk" : 0 ,
                    "C_Low Risk" : 0,
                    "C_AI-Powered Actions" : 0,
                    "C_Informative" : 0,
                    "CCaption" : "No Data", 
                    "ProcessingIntegrity" : modelResponse["processingIntegrity Score"],
                    "PI_High Risk" : modelResponse["PI_High Risk Score"] ,
                    "PI_Medium Risk" : modelResponse["PI_Medium Risk Score"] ,
                    "PI_Low Risk" : modelResponse["PI_Low Risk Score"],
                    "PI_AI-Powered Actions" : modelResponse["PI_AI-Powered Actions Score"],
                    "PI_Informative" : modelResponse["PI_Informative Score"],
                    "PICaption" : modelResponse["PICaption"],
                    "Privacy" : 0,
                    "P_Data Leak Alerts" : 0,
                    "P_Conset Monitoring" : 0,
                    "P_Encryption Enforcement" : 0,
                    "P_Audit Trail Tracking" : 0,
                    "P_Informative" : 0,
                    "PCaption" : "No Data"
                }
            )
        
        case "privacy":
            return jsonify(
                {
                    "Status_Code" : 200,
                    "Message" : "Analysis Result..",
                    "Security" : 0,
                    "S_High Risk" : 0,
                    "S_Medium Risk" : 0,
                    "S_Low Risk" : 0,
                    "S_AI-Powered Actions" : 0,
                    "S_Informative" : 0,
                    "SCaption" : "No Data",
                    "Availability" : 0,
                    "A_High Risk" : 0,
                    "A_Medium Risk" : 0,
                    "A_Low Risk" : 0,
                    "A_AI-Powered Actions" : 0,
                    "A_Informative" : 0,
                    "ACaption" : "No Data",                    
                    "Confidentiality" : 0,
                    "C_High Risk" : 0 ,
                    "C_Medium Risk" : 0 ,
                    "C_Low Risk" : 0,
                    "C_AI-Powered Actions" : 0,
                    "C_Informative" : 0,
                    "CCaption" : "No Data", 
                    "ProcessingIntegrity" : 0,
                    "PI_High Risk" : 0 ,
                    "PI_Medium Risk" : 0 ,
                    "PI_Low Risk" : 0,
                    "PI_AI-Powered Actions" : 0,
                    "PI_Informative" : 0,
                    "PICaption" : "No Data",
                    "Privacy" : modelResponse["privacy Score"],
                    "P_Data Leak Alerts" : modelResponse["P_Data Leak Alerts Score"],
                    "P_Conset Monitoring" : modelResponse["P_Conset Monitoring Score"],
                    "P_Encryption Enforcement" : modelResponse["P_Encryption Enforcement Score"],
                    "P_Audit Trail Tracking" : modelResponse["P_Audit Trail Tracking Score"],
                    "P_Informative" : modelResponse["P_Informative Score"],
                    "PCaption" : modelResponse["PCaption"]
                }
            )
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT or default to 5000 locally
    app.run(host='0.0.0.0', port=port, debug=False)



