const BaseOption = {
    Decimal: 10,
    Hex: 16,
    Octal: 8
}

const config = {
    base: BaseOption.Decimal,
}

const isValidDecimal = /^([01]?\d{0,2}|2[0-4]\d|25[0-5])$/;
const isValidHex = /^((0x|0X)?[0-9A-Fa-f]{0,2})$/;
const isValidOctal = /^(0o|0O|0)?([0-3]?[0-7]{0,2})$/;
const isAlphanumeric = /^[a-zA-Z0-9]$/;

const IPAddress = {
    octets: [0, 0, 0, 0],
};

function getDisplayOctet(octetIndex) {
    if (!isValidOctetIndex(octetIndex)) {
        return null;
    }

    const value = IPAddress.octets[octetIndex].toString(config.base);

    switch(config.base) {
        case BaseOption.Hex:
            return value.padStart(2, '0').toUpperCase();
        case BaseOption.Octal:
            return IPAddress.octets[octetIndex] === 0 ? value : "0" + value;
        default:
            return value;
    }
}

function isValidOctetIndex(octetIndex) {
    return octetIndex >= 0 && octetIndex <= 3;
}

function updateOctetField(octetIndex) {
    if (!isValidOctetIndex(octetIndex)) {
        return;
    }

    let octetField = document.getElementById(`octet${octetIndex + 1}`);
    octetField.value = getDisplayOctet(octetIndex);
}

function updateOctetBase() {
    for (let octetIndex = 0; octetIndex < IPAddress.octets.length; octetIndex++) {
        updateOctetField(octetIndex);
    }
}

// Function to toggle a specific bit within an octet
function toggleBit(octetIndex, bitIndex) {
    IPAddress.octets[octetIndex] ^= (1 << bitIndex);
    updateOctetField(octetIndex);
    setBitStatus(octetIndex, bitIndex);
}

function setBitStatus(octetIndex, bitIndex) {
    // Update the button label (0 or 1)
    const buttonElement = document.getElementById(`bit${octetIndex * 8 + bitIndex}`);
    const isBitActive = (IPAddress.octets[octetIndex] & (1 << bitIndex)) !== 0;

    // Toggle the "active" class to change the style
    buttonElement.classList.toggle("active", isBitActive);

    // Update the button text content
    buttonElement.textContent = isBitActive ? "1" : "0";
}

function toggleOctetBits(octetIndex) {
    for (let bitIndex = 0; bitIndex < 8; bitIndex++) {
        setBitStatus(octetIndex, bitIndex);
    }
}


updateOctetBase();
for (let octetIndex = 0; octetIndex < IPAddress.octets.length; octetIndex++) {
    for (let bitIndex = 0; bitIndex < 8; bitIndex++) {
        document.getElementById(`bit${octetIndex * 8 + bitIndex}`).addEventListener("click", function () {
            toggleBit(octetIndex, bitIndex);
        });
    }

    let octetInputField = document.getElementById(`octet${octetIndex + 1}`);

    octetInputField.addEventListener("focus", (e) => {
        if (IPAddress.octets[octetIndex] === 0) {
          e.target.value = "";
        }
      });

    octetInputField.addEventListener("blur", (e) => {
        if (e.target.value === "") {
          e.target.value = getDisplayOctet(octetIndex);
        }
    });

    octetInputField.addEventListener("change", (e) => {
        const newValue = parseInt(e.target.value, config.base);

        if (!isNaN(newValue) && newValue >= 0 && newValue <= 255) {
            IPAddress.octets[octetIndex] = newValue;
            toggleOctetBits(octetIndex);
        }

        e.target.value = getDisplayOctet(octetIndex);
      });

      octetInputField.addEventListener("keydown", (e) => {
        const re = config.base === BaseOption.Hex ? isValidHex : config.base === BaseOption.Octal ? isValidOctal : isValidDecimal;  
        const newValue = e.key === "Backspace" ? e.target.value.slice(0, -1) : e.target.value + (isAlphanumeric.test(e.key) ? e.key : "");
        console.log(newValue);

        if (!re.test(newValue)) {
            e.preventDefault();
        }
      });


    document.getElementById(`clear-octet${octetIndex + 1}`).addEventListener("click", function() {
        IPAddress.octets[octetIndex] = 0;
        octetInputField.value = "0";
        toggleOctetBits(octetIndex);
        octetInputField.focus();
      });
}