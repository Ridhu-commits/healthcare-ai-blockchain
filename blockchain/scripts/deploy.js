const hre = require("hardhat");

async function main() {
  const predictionFactory = await hre.ethers.getContractFactory("HealthcarePrediction");
  const predictionContract = await predictionFactory.deploy();

  await predictionContract.waitForDeployment();

  console.log("HealthcarePrediction deployed to:", await predictionContract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
