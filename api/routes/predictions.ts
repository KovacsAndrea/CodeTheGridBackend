import express from "express";
import { Prediction } from "../../core/models/Prediction";
import { PredictionController } from "../../core/controllers/predictionController";

const predictionRouter = express.Router();
const predictionController = new PredictionController()

predictionRouter.get("/", async (_req, _res) => {
    try {
        const prediction: Prediction = await predictionController.generatePrediction();
        _res.status(200).json({ prediction });
      } catch (err) {
        _res.status(500).json({ error: 'Failed to generate prediction', details: err });
      }
});

export default predictionRouter;