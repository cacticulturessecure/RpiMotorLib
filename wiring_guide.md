# Roomba Motor Control - Wiring Guide

## Hardware Components
- Raspberry Pi 4
- L298N H-Bridge Motor Driver Module
- 18V Ryobi Battery with 20A fuse
- Two Roomba motors
- Jumper wires

## Critical Setup Steps

### 1. L298N Module Preparation
**IMPORTANT**: Remove the 12V jumper from the L298N module before connecting 18V power supply!

### 2. Power Connections
```
18V Ryobi Battery (+) → L298N Pin 4 (VCC)
18V Ryobi Battery (-) → L298N Pin 5 (GND)
Pi GND → L298N Pin 5 (GND) - CRITICAL for common ground
```

### 3. Motor Connections
```
Left Roomba Motor → L298N Motor A (Pins 1 & 2)
Right Roomba Motor → L298N Motor B (Pins 13 & 14)
```

### 4. GPIO Pin Connections (Pi 4 → L298N)
```
GPIO 19 → IN1 (Motor A direction)
GPIO 13 → IN2 (Motor A direction)
GPIO 26 → ENA (Motor A enable/speed) - Remove jumper first
GPIO 21 → IN3 (Motor B direction)
GPIO 20 → IN4 (Motor B direction)
GPIO 16 → ENB (Motor B enable/speed) - Remove jumper first
```

## L298N Module Pin Reference
```
Pin 1:  Motor A (+)
Pin 2:  Motor A (-)
Pin 3:  12V Jumper - REMOVE for 18V supply
Pin 4:  VCC (18V input)
Pin 5:  GND
Pin 6:  5V output (only if 12V jumper present)
Pin 7:  ENA (Motor A enable)
Pin 8:  IN1 (Motor A control)
Pin 9:  IN2 (Motor A control)
Pin 10: IN3 (Motor B control)
Pin 11: IN4 (Motor B control)
Pin 12: ENB (Motor B enable)
Pin 13: Motor B (+)
Pin 14: Motor B (-)
```

## Safety Precautions
1. Always connect ground first
2. Double-check polarity before powering on
3. Start with low speeds (15-25%) for testing
4. Keep 20A fuse in battery circuit
5. Have emergency stop accessible
6. Test individual motors before running together

## Testing Steps
1. Connect all wiring according to guide
2. Run basic connectivity test
3. Test individual motor directions
4. Test speed control
5. Test coordinated movement

## Troubleshooting
- Motors not turning: Check enable pin connections and jumper removal
- Motors turning wrong direction: Swap motor wire polarity
- No response: Verify GPIO pin assignments match code
- Overheating: Reduce duty cycle, check for shorts