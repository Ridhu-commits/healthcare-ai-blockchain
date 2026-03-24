// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract HealthcarePrediction {
    struct Prediction {
        string patientHash;
        uint256 age;
        uint256 bloodPressure;
        uint256 sugarLevel;
        string riskLevel;
        uint256 timestamp;
    }

    mapping(string => Prediction[]) private predictionsByPatient;

    event PredictionStored(
        string patientHash,
        uint256 age,
        uint256 bloodPressure,
        uint256 sugarLevel,
        string riskLevel,
        uint256 timestamp
    );

    function storePrediction(
        string memory patientHash,
        uint256 age,
        uint256 bloodPressure,
        uint256 sugarLevel,
        string memory riskLevel
    ) public {
        Prediction memory newPrediction = Prediction({
            patientHash: patientHash,
            age: age,
            bloodPressure: bloodPressure,
            sugarLevel: sugarLevel,
            riskLevel: riskLevel,
            timestamp: block.timestamp
        });

        predictionsByPatient[patientHash].push(newPrediction);

        emit PredictionStored(
            patientHash,
            age,
            bloodPressure,
            sugarLevel,
            riskLevel,
            block.timestamp
        );
    }

    function getPredictionCount(string memory patientHash) public view returns (uint256) {
        return predictionsByPatient[patientHash].length;
    }

    function getPrediction(
        string memory patientHash,
        uint256 index
    )
        public
        view
        returns (
            string memory,
            uint256,
            uint256,
            uint256,
            string memory,
            uint256
        )
    {
        Prediction memory prediction = predictionsByPatient[patientHash][index];
        return (
            prediction.patientHash,
            prediction.age,
            prediction.bloodPressure,
            prediction.sugarLevel,
            prediction.riskLevel,
            prediction.timestamp
        );
    }
}
