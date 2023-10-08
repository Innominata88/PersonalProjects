const BaseOption = {
    Decimal: 10,
    Hex: 16,
    Octal: 8
}

const config = {
    base: BaseOption.Decimal
}


class OctetStructure {
    static isValidDecimal = /^([01]?\d{0,2}|2[0-4]\d|25[0-5])$/;
    static isValidHex = /^((0x|0X)?[0-9A-Fa-f]{0,2})$/;
    static isValidOctal = /^(0o|0O|0)?([0-3]?[0-7]{0,2})$/;
    static isAlphanumeric = /^[a-zA-Z0-9]$/;
    static ordinals = ['First', 'Second', 'Third', 'Fourth'];

  constructor(container, octetNumber, updateCallback) {
    this.container = container;
    this.octetNumber = octetNumber;
    this.updateCallback = updateCallback;
    
    this.createOctetStructure();
    this.setOctetValue(0);
  }

  createOctetStructure() {
    const octetContainer = document.createElement('div');
    octetContainer.classList.add('octet-container', `octet-${this.octetNumber}`);

    const octetHeader = document.createElement('div');
    octetHeader.classList.add('octet-header');
    octetHeader.textContent = `${OctetStructure.ordinals[this.octetNumber - 1]} Octet`;
    
    const octetTextbox = document.createElement('div');
    octetTextbox.classList.add('octet-textbox');
    
    const inputField = document.createElement('input');
    inputField.setAttribute('type', 'text');
    inputField.setAttribute('tabindex', this.octetNumber);
    inputField.classList.add('octet-input-field');
    inputField.addEventListener('focus', (e) => this.clearZeroOnFocus(e.target));
    inputField.addEventListener('blur', (e) => this.resetEmptyOctetValue(e.target));
    inputField.addEventListener('change', (e) => this.processOctetFieldChange(e.target));
    inputField.addEventListener('keydown', (e) => this.validateOctetInputKey(e));
    
    const clearButton = document.createElement('span');
    clearButton.classList.add('clear-button');
    clearButton.textContent = '\u2715';
    clearButton.addEventListener('click', () => this.clearOctet());

    octetTextbox.appendChild(inputField);
    octetTextbox.appendChild(clearButton);

    octetContainer.appendChild(octetHeader);
    octetContainer.appendChild(octetTextbox);

    const octet = document.createElement('div');
    octet.classList.add('octet', `octet-${this.octetNumber}`);

    const bitLabelContainer = document.createElement('div');
    bitLabelContainer.classList.add('octet');

    for (let i = 7; i >= 0; i--) {
      const bitButton = document.createElement('button');
      bitButton.classList.add('bit');
      bitButton.textContent = '0';
      bitButton.title = Math.pow(2, i);
      bitButton.addEventListener('click', () => this.toggleBit(bitButton, i));
      octet.appendChild(bitButton);

      const bitLabel = document.createElement('span');
      const bitNumber = (8 * (this.octetNumber - 1)) + (7 - i);
      bitLabel.classList.add('bitlabel');
      bitLabel.textContent = bitNumber;
      bitLabelContainer.appendChild(bitLabel);
    }

    octetContainer.appendChild(octet);
    octetContainer.appendChild(bitLabelContainer);

    this.container.appendChild(octetContainer);
  }

  setOctetValue(newValue) {
    this.octetValue = newValue;
    this.setDisplayOctet();
    this.updateCallback(this.octetValue);
  }

  // Reset the octet field and bit buttons to 0
  clearOctet() {
    if (this.octetValue !== 0) {
        this.setOctetValue(0);
        this.toggleOctetBits();
    }
  }

  toggleOctetBits() {
    const bitButtons = document.querySelector(`.octet-container.octet-${this.octetNumber}`).querySelectorAll('.bit');

    for(let bitIndex = 0; bitIndex < 8; bitIndex++) {
        this.setBitButton(bitButtons[bitIndex], (7 - bitIndex));
    }

  }

  toggleBit(bitButton, bitIndex) {
    console.log(bitIndex);
    console.log(bitButton);
    // Toggle the bit (0 to 1 or 1 to 0)
    this.setOctetValue(this.setBit(bitIndex));
    this.setBitButton(bitButton, bitIndex);
  }

  setBitButton(bitButton, bitIndex) {
    bitButton.textContent = this.getBit(bitIndex);
    bitButton.classList.toggle("active", bitButton.textContent !== '0');
  }

  setBit(bitIndex) {
    return this.octetValue ^ 1 << bitIndex;
  }

  getBit(bitIndex) {
    return (this.octetValue >> bitIndex) & 1;
  }
  
  /*
    Update the input field with the current octet value. 
    Callers of this function are responsible for updating the bit buttons as appropriate to cut down on unecessary updates.
  */
  setDisplayOctet() {
    const octetField = this.container.querySelector(`.octet-${this.octetNumber} .octet-input-field`);
    octetField.value = this.getDisplayOctet();
  }

  // Returns the string representation of this octet's value in the desired base
  getDisplayOctet() {
    const value = this.octetValue.toString(config.base);

    switch(config.base) {
        case BaseOption.Hex:
            return value.padStart(2, '0').toUpperCase();
        case BaseOption.Octal:
            return IPAddress.octets[octetIndex] === 0 ? value : "0" + value;
        default:
            return value;
        }
    }

    clearZeroOnFocus(octetField) {
        if (this.octetValue === 0) {
            octetField.value = "";
        }
    }

    resetEmptyOctetValue(octetField) {
        if (octetField.value === "") {
            octetField.value = this.getDisplayOctet();
        }
    }

    processOctetFieldChange(octetField) {
        const newValue = parseInt(octetField.value, config.base);

        if(this.isValidOctetValue(newValue)) {
            this.setOctetValue(newValue);
            this.toggleOctetBits();
        }
        else {
            this.setDisplayOctet();
        }

    }

    isValidOctetValue(octetValue) {
        return !isNaN(octetValue) && octetValue >= 0 && octetValue <= 255;
    }

    isValidOctetInput(octetValue) {
        switch(config.base){
            case BaseOption.Hex:
                return OctetStructure.isValidHex.test(octetValue);
            case BaseOption.Octal:
                return OctetStructure.isValidOctal.test(octetValue);
            default:
                return OctetStructure.isValidDecimal.test(octetValue);
        }
    }

    validateOctetInputKey(event) {
        const newValue = event.key === "Backspace" ? event.target.value.slice(0, -1) : 
                        event.target.value + (OctetStructure.isAlphanumeric.test(event.key) ? event.key : "");
        console.log(newValue);

        if(!this.isValidOctetInput(newValue)) {
            event.preventDefault();
        }
    }

}


class OctetGroup {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.octetValues = [0, 0, 0, 0];
        this.octetStructures = [];
        this.createOctetGroupStructure();
    }

    createOctetGroupStructure() {
        const octetGroup = document.createElement('div');
        octetGroup.classList.add('octet-group');

        for (let i = 1; i <= 4; i++) {
            const updateCallback = (value) => {
                this.octetValues[i - 1] = value;
                console.log(this.octetValues);
              };
            const octetStructure = new OctetStructure(octetGroup, i, updateCallback);

            this.octetStructures.push(octetStructure);
            
            if (i < 4) {
                const dotDiv = document.createElement('div');
                dotDiv.classList.add('dot-div');
                dotDiv.textContent = '.';
                octetGroup.appendChild(dotDiv);
            }
        }

        this.container.appendChild(octetGroup);
    }
}


// Testing
new OctetGroup('formContainer');