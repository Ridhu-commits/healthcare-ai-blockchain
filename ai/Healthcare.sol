// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Healthcare {

    struct Record {
        string patientId;
        uint heartRate;
        uint systolicBP;
        string diagnosis;
        uint timestamp;
    }

    mapping(string => Record[]) public records;

    event RecordStored(
        string patientId,
        uint heartRate,
        uint systolicBP,
        uint timestamp
    );

    function addRecord(
        string memory patientId,
        uint heartRate,
        uint systolicBP,
        string memory diagnosis
    ) public {
        records[patientId].push(
            Record(
                patientId,
                heartRate,
                systolicBP,
                diagnosis,
                block.timestamp
            )
        );

        emit RecordStored(
            patientId,
            heartRate,
            systolicBP,
            block.timestamp
        );
    }

    function getRecordCount(string memory patientId)
        public view returns (uint)
    {
        return records[patientId].length;
    }

    function getRecord(string memory patientId, uint index)
        public view returns (
            string memory,
            uint,
            uint,
            string memory,
            uint
        )
    {
        Record memory r = records[patientId][index];
        return (
            r.patientId,
            r.heartRate,
            r.systolicBP,
            r.diagnosis,
            r.timestamp
        );
    }
}