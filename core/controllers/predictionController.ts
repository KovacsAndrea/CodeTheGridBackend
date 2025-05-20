import { spawn } from "child_process";
import { Prediction } from "../models/Prediction";

export class PredictionController {
    private prediction: Prediction;
  
    constructor() {
      this.prediction = {
        AlexAlbon: '0',
        CarlosSainz: '0',
        Constructor: '0',
      };
    }
  
    public async generatePrediction(): Promise<Prediction> {
      const result = await this.runPythonModel();
      this.prediction = result;
      return result;
    }

    private runPythonModel(): Promise<Prediction> {
      return new Promise((resolve, reject) => {
        const py = spawn('python', ['core/py/predict.py']);
  
        py.stdin.write(JSON.stringify({}));
        py.stdin.end();
  
        let data = '';
        py.stdout.on('data', (chunk) => {
          data += chunk.toString();
        });
  
        py.stderr.on('data', (err) => {
          console.error('Python error:', err.toString());
          reject(err.toString());
        });
  
        py.on('close', () => {
          try {
            const prediction: Prediction = JSON.parse(data);
            resolve(prediction);
          } catch (e) {
            reject(`Failed to parse Python output: ${e}`);
          }
        });
      });
    }
  
    public getPrediction(): Prediction {
      return this.prediction;
    }
  }