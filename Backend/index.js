const express = require("express");
const app = express();
const authRoutes = require("./routes/auth");
const dashboardRoutes = require("./routes/dashboard");
const stockRoutes = require("./routes/stocks");
const verifyToken = require("./routes/validate-token");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const cors = require("cors");

dotenv.config();
app.use(express.json());

dotenv.config();
app.use(cors());

mongoose.connect(
process.env.DB_CONNECT,
{
  useNewUrlParser: true,
  useUnifiedTopology: true,
},
() => console.log("connected to db")
);

app.use("/api", authRoutes);
app.use("/api/dashboard", verifyToken, dashboardRoutes);
app.use("/api/stocks", stockRoutes);

app.listen(3001, () => console.log("server is running..."));