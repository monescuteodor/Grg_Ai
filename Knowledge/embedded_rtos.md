Embedded Systems & RTOS Complete Reference
CHAPTER 1: GETTING STARTED WITH EMBEDDED SYSTEMS
Remarks
Embedded systems are specialized computing systems dedicated to specific functions within larger mechanical/electrical systems. Key characteristics: real-time constraints, limited resources (RAM, flash, power), reliability requirements, direct hardware interaction. Applications: automotive (ECU), aerospace (flight control), IoT devices, medical devices, industrial automation, consumer electronics.
Tools: C/C++ (primary languages), ARM GCC toolchain, STM32CubeIDE, Keil MDK, IAR Embedded Workbench, OpenOCD (debugging), GDB, logic analyzers, oscilloscopes.
Hello Embedded (Blinky)
// blinky.c - LED blink on STM32 (bare-metal)
#include "stm32f4xx.h"

// Simple delay function (busy-wait)
void delay(volatile uint32_t count) {
    while (count--) {
        __asm__ __volatile__ ("nop");
    }
}

int main(void) {
    // Enable GPIOA clock (RCC_AHB1ENR register)
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    
    // Configure PA5 as output (Arduino LED pin on Nucleo)
    GPIOA->MODER &= ~(3UL << (5 * 2));  // Clear mode bits
    GPIOA->MODER |= (1UL << (5 * 2));   // Set to output mode
    
    // Main loop
    while (1) {
        GPIOA->ODR ^= (1UL << 5);  // Toggle PA5
        delay(500000);              // Wait
    }
    
    return 0;  // Never reached
}

// Build and flash:
// arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -O2 -o blinky.elf blinky.c
// arm-none-eabi-objcopy -O binary blinky.elf blinky.bin
// st-flash write blinky.bin 0x08000000

Embedded System Architecture
# Typical embedded system components:
# - Microcontroller (MCU) or Microprocessor (MPU)
# - Memory: Flash (program), SRAM (data), EEPROM (persistent)
# - Peripherals: GPIO, UART, SPI, I2C, ADC, DAC, Timers, PWM
# - Clock sources: HSE (external crystal), HSI (internal RC), LSE, LSI
# - Power management: LDO, DC-DC converters, battery management
# - Debug interfaces: SWD, JTAG, UART

# Memory map example (STM32F4):
# 0x0000_0000 - 0x1FFF_FFFF: Code (Flash)
# 0x2000_0000 - 0x2001_FFFF: SRAM (128KB)
# 0x4000_0000 - 0x5FFF_FFFF: Peripherals
# 0xE000_0000 - 0xE00F_FFFF: Cortex-M4 internal (NVIC, SysTick)

# Development workflow:
# 1. Write code (C/C++/Assembly)
# 2. Compile → ELF file
# 3. Link with startup code and libraries
# 4. Generate binary/hex file
# 5. Flash to MCU via SWD/JTAG/UART bootloader
# 6. Debug with GDB + OpenOCD or IDE

CHAPTER 2: ARM ARCHITECTURE BASICS
ARM Cortex-M Overview
# ARM Cortex-M family: M0, M0+, M3, M4, M7, M23, M33, M55, M85
# Key features:
# - Harvard architecture (separate instruction/data buses)
# - Thumb-2 instruction set (16-bit and 32-bit mixed)
# - Nested Vectored Interrupt Controller (NVIC)
# - SysTick timer for RTOS
# - Memory Protection Unit (MPU) - M3 and above
# - Optional FPU (M4F, M7F)

# Register set (Cortex-M4):
# R0-R12: General purpose registers
# R13 (SP): Stack Pointer (MSP = Main, PSP = Process)
# R14 (LR): Link Register (return address)
# R15 (PC): Program Counter
# xPSR: Program Status Register (N, Z, C, V, Q flags)
# PRIMASK, FAULTMASK, BASEPRI: Interrupt mask registers

ARM Assembly Basics
; arm_assembly.s - Basic ARM assembly examples

; Function: add two numbers
; uint32_t add(uint32_t a, uint32_t b)
; Parameters: R0 = a, R1 = b
; Return: R0 = result
.global add
add:
    ADD R0, R0, R1    ; R0 = R0 + R1
    BX LR              ; Return (Branch to Link Register)

; Function: multiply using shift-and-add
; uint32_t multiply(uint32_t a, uint32_t b)
.global multiply
multiply:
    MOV R2, #0         ; R2 = result = 0
    MOV R3, #0         ; R3 = counter = 0
    
.loop:
    CMP R3, R1         ; Compare counter with b
    BGE .done          ; If counter >= b, exit loop
    
    ADD R2, R2, R0     ; result += a
    ADD R3, R3, #1     ; counter++
    B .loop            ; Repeat
    
.done:
    MOV R0, R2         ; Return result in R0
    BX LR

; Function: bit manipulation
; uint32_t set_bit(uint32_t value, uint8_t bit)
.global set_bit
set_bit:
    MOV R2, #1
    LSL R2, R2, R1     ; R2 = 1 << bit
    ORR R0, R0, R2     ; value |= (1 << bit)
    BX LR

; Function: clear bit
; uint32_t clear_bit(uint32_t value, uint8_t bit)
.global clear_bit
clear_bit:
    MOV R2, #1
    LSL R2, R2, R1     ; R2 = 1 << bit
    MVN R2, R2         ; R2 = ~(1 << bit)
    AND R0, R0, R2     ; value &= ~(1 << bit)
    BX LR

; Function: toggle bit
; uint32_t toggle_bit(uint32_t value, uint8_t bit)
.global toggle_bit
toggle_bit:
    MOV R2, #1
    LSL R2, R2, R1     ; R2 = 1 << bit
    EOR R0, R0, R2     ; value ^= (1 << bit)
    BX LR

Memory-Mapped I/O
// memory_mapped_io.c - Direct register access
#include "stm32f4xx.h"

// GPIO register structure (from CMSIS)
typedef struct {
    volatile uint32_t MODER;    // Mode register (offset 0x00)
    volatile uint32_t OTYPER;   // Output type (offset 0x04)
    volatile uint32_t OSPEEDR;  // Output speed (offset 0x08)
    volatile uint32_t PUPDR;    // Pull-up/pull-down (offset 0x0C)
    volatile uint32_t IDR;      // Input data (offset 0x10)
    volatile uint32_t ODR;      // Output data (offset 0x14)
    volatile uint32_t BSRR;     // Bit set/reset (offset 0x18)
    volatile uint32_t LCKR;     // Lock register (offset 0x1C)
    volatile uint32_t AFR[2];   // Alternate function (offset 0x20)
} GPIO_TypeDef;

// Base addresses (from reference manual)
#define GPIOA_BASE  0x40020000UL
#define GPIOB_BASE  0x40020400UL
#define GPIOC_BASE  0x40020800UL

#define GPIOA  ((GPIO_TypeDef *) GPIOA_BASE)
#define GPIOB  ((GPIO_TypeDef *) GPIOB_BASE)
#define GPIOC  ((GPIO_TypeDef *) GPIOC_BASE)

// RCC register structure
typedef struct {
    volatile uint32_t CR;           // Clock control (offset 0x00)
    volatile uint32_t PLLCFGR;      // PLL config (offset 0x04)
    volatile uint32_t CFGR;         // Clock config (offset 0x08)
    volatile uint32_t CIR;          // Clock interrupt (offset 0x0C)
    volatile uint32_t AHB1RSTR;     // AHB1 reset (offset 0x10)
    volatile uint32_t AHB2RSTR;     // AHB2 reset (offset 0x14)
    volatile uint32_t AHB3RSTR;     // AHB3 reset (offset 0x18)
    volatile uint32_t RESERVED0;    // Reserved (offset 0x1C)
    volatile uint32_t APB1RSTR;     // APB1 reset (offset 0x20)
    volatile uint32_t APB2RSTR;     // APB2 reset (offset 0x24)
    volatile uint32_t RESERVED1[2]; // Reserved
    volatile uint32_t AHB1ENR;      // AHB1 enable (offset 0x30)
    volatile uint32_t AHB2ENR;      // AHB2 enable (offset 0x34)
    volatile uint32_t AHB3ENR;      // AHB3 enable (offset 0x38)
    volatile uint32_t RESERVED2;    // Reserved
    volatile uint32_t APB1ENR;      // APB1 enable (offset 0x40)
    volatile uint32_t APB2ENR;      // APB2 enable (offset 0x44)
} RCC_TypeDef;

#define RCC_BASE  0x40023800UL
#define RCC  ((RCC_TypeDef *) RCC_BASE)

// Bit definitions
#define RCC_AHB1ENR_GPIOAEN  (1UL << 0)
#define RCC_AHB1ENR_GPIOBEN  (1UL << 1)
#define RCC_AHB1ENR_GPIOCEN  (1UL << 2)

// Example: Configure PA5 as output using direct register access
void configure_gpio(void) {
    // Enable GPIOA clock
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    
    // Configure PA5 as output
    GPIOA->MODER &= ~(3UL << (5 * 2));  // Clear bits 10-11
    GPIOA->MODER |= (1UL << (5 * 2));   // Set to output (01)
    
    // Set output speed to high
    GPIOA->OSPEEDR &= ~(3UL << (5 * 2));
    GPIOA->OSPEEDR |= (2UL << (5 * 2)); // High speed (10)
    
    // No pull-up/pull-down
    GPIOA->PUPDR &= ~(3UL << (5 * 2));
}

// Example: Toggle LED using BSRR register (atomic operation)
void toggle_led_bsrr(void) {
    // BSRR allows setting/resetting bits atomically
    // Lower 16 bits: set bits (write 1 to set)
    // Upper 16 bits: reset bits (write 1 to reset)
    
    static uint8_t state = 0;
    if (state) {
        GPIOA->BSRR = (1UL << (5 + 16));  // Reset PA5 (bits 16-31)
        state = 0;
    } else {
        GPIOA->BSRR = (1UL << 5);         // Set PA5 (bits 0-15)
        state = 1;
    }
}

CHAPTER 3: MEMORY AND PERIPHERALS
GPIO Configuration
// gpio_config.c - Comprehensive GPIO configuration
#include "stm32f4xx.h"

// GPIO modes
#define GPIO_MODE_INPUT    0x00
#define GPIO_MODE_OUTPUT   0x01
#define GPIO_MODE_AF       0x02  // Alternate function
#define GPIO_MODE_ANALOG   0x03

// Output types
#define GPIO_OTYPE_PP      0x00  // Push-pull
#define GPIO_OTYPE_OD      0x01  // Open-drain

// Output speeds
#define GPIO_SPEED_LOW     0x00
#define GPIO_SPEED_MEDIUM  0x01
#define GPIO_SPEED_HIGH    0x02
#define GPIO_SPEED_VERY_HIGH 0x03

// Pull-up/pull-down
#define GPIO_PUPD_NONE     0x00
#define GPIO_PUPD_UP       0x01
#define GPIO_PUPD_DOWN     0x02

void gpio_init(GPIO_TypeDef *gpio, uint8_t pin, uint8_t mode, 
               uint8_t otype, uint8_t speed, uint8_t pupd) {
    // Configure mode
    gpio->MODER &= ~(3UL << (pin * 2));
    gpio->MODER |= (mode << (pin * 2));
    
    // Configure output type
    gpio->OTYPER &= ~(1UL << pin);
    gpio->OTYPER |= (otype << pin);
    
    // Configure speed
    gpio->OSPEEDR &= ~(3UL << (pin * 2));
    gpio->OSPEEDR |= (speed << (pin * 2));
    
    // Configure pull-up/pull-down
    gpio->PUPDR &= ~(3UL << (pin * 2));
    gpio->PUPDR |= (pupd << (pin * 2));
}

void gpio_set_af(GPIO_TypeDef *gpio, uint8_t pin, uint8_t af) {
    // Alternate function registers: AFR[0] for pins 0-7, AFR[1] for pins 8-15
    uint8_t reg_idx = pin / 8;
    uint8_t pos = (pin % 8) * 4;
    
    gpio->AFR[reg_idx] &= ~(0xFUL << pos);
    gpio->AFR[reg_idx] |= (af << pos);
}

// Example: Configure PA2 as USART2_TX (AF7)
void configure_uart_pins(void) {
    // Enable GPIOA clock
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    
    // PA2: USART2_TX
    gpio_init(GPIOA, 2, GPIO_MODE_AF, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_UP);
    gpio_set_af(GPIOA, 2, 7);  // AF7 = USART2
    
    // PA3: USART2_RX
    gpio_init(GPIOA, 3, GPIO_MODE_AF, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_UP);
    gpio_set_af(GPIOA, 3, 7);
}

UART Configuration
// uart.c - UART driver implementation
#include "stm32f4xx.h"

// USART2 register structure
typedef struct {
    volatile uint32_t SR;    // Status register
    volatile uint32_t DR;    // Data register
    volatile uint32_t BRR;   // Baud rate register
    volatile uint32_t CR1;   // Control register 1
    volatile uint32_t CR2;   // Control register 2
    volatile uint32_t CR3;   // Control register 3
    volatile uint32_t GTPR;  // Guard time and prescaler
} USART_TypeDef;

#define USART2_BASE  0x40004400UL
#define USART2  ((USART_TypeDef *) USART2_BASE)

// Status register bits
#define USART_SR_TXE   (1UL << 7)  // Transmit data register empty
#define USART_SR_TC    (1UL << 6)  // Transmission complete
#define USART_SR_RXNE  (1UL << 5)  // Read data register not empty

// Control register 1 bits
#define USART_CR1_UE    (1UL << 13)  // USART enable
#define USART_CR1_TE    (1UL << 3)   // Transmitter enable
#define USART_CR1_RE    (1UL << 2)   // Receiver enable
#define USART_CR1_RXNEIE (1UL << 5)  // RXNE interrupt enable

void uart_init(uint32_t baudrate) {
    // Enable GPIOA and USART2 clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB1ENR |= (1UL << 17);  // USART2EN (bit 17)
    
    // Configure PA2 (TX) and PA3 (RX)
    configure_uart_pins();
    
    // Configure baud rate
    // BRR = fCK / (16 * baudrate)
    // For STM32F4: fCK = 16 MHz (APB1 default)
    uint32_t pclk1 = 16000000;  // 16 MHz
    USART2->BRR = pclk1 / baudrate;
    
    // Configure USART: 8 bits, 1 stop bit, no parity
    USART2->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
}

void uart_send_char(char c) {
    // Wait until transmit register is empty
    while (!(USART2->SR & USART_SR_TXE));
    
    // Write character to data register
    USART2->DR = c;
}

void uart_send_string(const char *str) {
    while (*str) {
        if (*str == '\n') {
            uart_send_char('\r');  // Add carriage return
        }
        uart_send_char(*str++);
    }
}

char uart_receive_char(void) {
    // Wait until data is received
    while (!(USART2->SR & USART_SR_RXNE));
    
    return (char)(USART2->DR & 0xFF);
}

int uart_receive_string(char *buffer, int max_len) {
    int i = 0;
    while (i < max_len - 1) {
        char c = uart_receive_char();
        if (c == '\r' || c == '\n') {
            break;
        }
        buffer[i++] = c;
    }
    buffer[i] = '\0';
    return i;
}

// Example usage
int main(void) {
    uart_init(115200);
    
    uart_send_string("Hello, UART!\r\n");
    
    char buffer[64];
    uart_send_string("Enter text: ");
    int len = uart_receive_string(buffer, sizeof(buffer));
    
    uart_send_string("You entered: ");
    uart_send_string(buffer);
    uart_send_string("\r\n");
    
    while (1) {
        // Echo received characters
        char c = uart_receive_char();
        uart_send_char(c);
    }
    
    return 0;
}

SPI Configuration
// spi.c - SPI master driver
#include "stm32f4xx.h"

// SPI1 register structure
typedef struct {
    volatile uint32_t CR1;      // Control register 1
    volatile uint32_t CR2;      // Control register 2
    volatile uint32_t SR;       // Status register
    volatile uint32_t DR;       // Data register
    volatile uint32_t CRCPR;    // CRC polynomial
    volatile uint32_t RXCRCR;   // RX CRC
    volatile uint32_t TXCRCR;   // TX CRC
    volatile uint32_t I2SCFGR;  // I2S configuration
    volatile uint32_t I2SPR;    // I2S prescaler
} SPI_TypeDef;

#define SPI1_BASE  0x40013000UL
#define SPI1  ((SPI_TypeDef *) SPI1_BASE)

// Status register bits
#define SPI_SR_RXNE  (1UL << 0)  // Receive buffer not empty
#define SPI_SR_TXE   (1UL << 1)  // Transmit buffer empty
#define SPI_SR_BSY   (1UL << 7)  // Busy flag

// Control register 1 bits
#define SPI_CR1_CPHA   (1UL << 0)   // Clock phase
#define SPI_CR1_CPOL   (1UL << 1)   // Clock polarity
#define SPI_CR1_MSTR   (1UL << 2)   // Master selection
#define SPI_CR1_BR     (7UL << 3)   // Baud rate control
#define SPI_CR1_SPE    (1UL << 6)   // SPI enable
#define SPI_CR1_SSI    (1UL << 8)   // Internal slave select
#define SPI_CR1_SSM    (1UL << 9)   // Software slave management

void spi_init(void) {
    // Enable GPIOA and SPI1 clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB2ENR |= (1UL << 12);  // SPI1EN (bit 12)
    
    // Configure SPI pins: PA5 (SCK), PA6 (MISO), PA7 (MOSI)
    // All as alternate function AF5 (SPI1)
    gpio_init(GPIOA, 5, GPIO_MODE_AF, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_NONE);
    gpio_init(GPIOA, 6, GPIO_MODE_AF, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_NONE);
    gpio_init(GPIOA, 7, GPIO_MODE_AF, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_NONE);
    
    gpio_set_af(GPIOA, 5, 5);  // AF5 = SPI1
    gpio_set_af(GPIOA, 6, 5);
    gpio_set_af(GPIOA, 7, 5);
    
    // Configure PA4 as NSS (manual control)
    gpio_init(GPIOA, 4, GPIO_MODE_OUTPUT, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_UP);
    GPIOA->BSRR = (1UL << 4);  // Set NSS high (deselect)
    
    // Configure SPI1
    // Baud rate = fPCLK2 / prescaler
    // For 16 MHz APB2, prescaler 16 → 1 MHz SPI clock
    SPI1->CR1 = SPI_CR1_MSTR |    // Master mode
                (4UL << 3) |      // BR = fPCLK/16 (prescaler 16)
                SPI_CR1_SSM |     // Software slave management
                SPI_CR1_SSI;      // Internal slave select high
    
    // Enable SPI
    SPI1->CR1 |= SPI_CR1_SPE;
}

void spi_select(void) {
    GPIOA->BSRR = (1UL << (4 + 16));  // Reset PA4 (select)
}

void spi_deselect(void) {
    GPIOA->BSRR = (1UL << 4);  // Set PA4 (deselect)
}

uint8_t spi_transfer(uint8_t data) {
    // Wait until transmit buffer is empty
    while (!(SPI1->SR & SPI_SR_TXE));
    
    // Write data
    SPI1->DR = data;
    
    // Wait until receive buffer is not empty
    while (!(SPI1->SR & SPI_SR_RXNE));
    
    // Read received data
    return (uint8_t)(SPI1->DR & 0xFF);
}

void spi_write(uint8_t *data, int len) {
    spi_select();
    for (int i = 0; i < len; i++) {
        spi_transfer(data[i]);
    }
    spi_deselect();
}

void spi_read(uint8_t *data, int len) {
    spi_select();
    for (int i = 0; i < len; i++) {
        data[i] = spi_transfer(0xFF);  // Send dummy byte to receive
    }
    spi_deselect();
}

// Example: Read from SPI device (e.g., SD card, sensor)
uint8_t spi_read_register(uint8_t reg) {
    spi_select();
    spi_transfer(reg | 0x80);  // Read command (bit 7 = 1)
    uint8_t value = spi_transfer(0xFF);  // Dummy byte to receive data
    spi_deselect();
    return value;
}

void spi_write_register(uint8_t reg, uint8_t value) {
    spi_select();
    spi_transfer(reg & 0x7F);  // Write command (bit 7 = 0)
    spi_transfer(value);
    spi_deselect();
}

I2C Configuration
// i2c.c - I2C master driver
#include "stm32f4xx.h"

// I2C1 register structure
typedef struct {
    volatile uint32_t CR1;      // Control register 1
    volatile uint32_t CR2;      // Control register 2
    volatile uint32_t OAR1;     // Own address register 1
    volatile uint32_t OAR2;     // Own address register 2
    volatile uint32_t DR;       // Data register
    volatile uint32_t SR1;      // Status register 1
    volatile uint32_t SR2;      // Status register 2
    volatile uint32_t CCR;      // Clock control register
    volatile uint32_t TRISE;    // Rise time register
    volatile uint32_t FLTR;     // Filter register
} I2C_TypeDef;

#define I2C1_BASE  0x40005400UL
#define I2C1  ((I2C_TypeDef *) I2C1_BASE)

// Control register 1 bits
#define I2C_CR1_PE     (1UL << 0)   // Peripheral enable
#define I2C_CR1_START  (1UL << 8)   // Start generation
#define I2C_CR1_STOP   (1UL << 9)   // Stop generation
#define I2C_CR1_ACK    (1UL << 10)  // Acknowledge enable

// Status register 1 bits
#define I2C_SR1_SB    (1UL << 0)    // Start bit
#define I2C_SR1_ADDR  (1UL << 1)    // Address sent
#define I2C_SR1_TXE   (1UL << 7)    // Transmit buffer empty
#define I2C_SR1_RXNE  (1UL << 6)    // Receive buffer not empty
#define I2C_SR1_AF    (1UL << 10)   // Acknowledge failure

void i2c_init(void) {
    // Enable GPIOB and I2C1 clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN;
    RCC->APB1ENR |= (1UL << 21);  // I2C1EN (bit 21)
    
    // Configure PB6 (SCL) and PB7 (SDA) as alternate function AF4 (I2C1)
    gpio_init(GPIOB, 6, GPIO_MODE_AF, GPIO_OTYPE_OD, GPIO_SPEED_HIGH, GPIO_PUPD_UP);
    gpio_init(GPIOB, 7, GPIO_MODE_AF, GPIO_OTYPE_OD, GPIO_SPEED_HIGH, GPIO_PUPD_UP);
    
    gpio_set_af(GPIOB, 6, 4);  // AF4 = I2C1
    gpio_set_af(GPIOB, 7, 4);
    
    // Reset I2C
    I2C1->CR1 = 0;
    
    // Configure clock
    // For 100 kHz I2C with 16 MHz APB1:
    // CCR = fPCLK1 / (2 * I2C_freq) = 16M / (2 * 100k) = 80
    I2C1->CR2 = 16;  // APB1 frequency in MHz
    I2C1->CCR = 80;  // Standard mode (100 kHz)
    I2C1->TRISE = 17;  // Max rise time = (300ns / 62.5ns) + 1 = 17
    
    // Enable I2C
    I2C1->CR1 |= I2C_CR1_PE;
}

void i2c_start(void) {
    I2C1->CR1 |= I2C_CR1_START;
    while (!(I2C1->SR1 & I2C_SR1_SB));  // Wait for start condition
}

void i2c_stop(void) {
    I2C1->CR1 |= I2C_CR1_STOP;
}

void i2c_send_address(uint8_t address, uint8_t read) {
    // Address is 7-bit, shifted left by 1, with R/W bit
    uint8_t addr = (address << 1) | (read ? 1 : 0);
    
    I2C1->DR = addr;
    while (!(I2C1->SR1 & I2C_SR1_ADDR));  // Wait for address sent
    
    // Clear ADDR flag by reading SR1 then SR2
    volatile uint32_t temp = I2C1->SR1;
    temp = I2C1->SR2;
    (void)temp;
}

void i2c_send_byte(uint8_t data) {
    while (!(I2C1->SR1 & I2C_SR1_TXE));  // Wait for transmit buffer empty
    I2C1->DR = data;
}

uint8_t i2c_receive_byte(uint8_t ack) {
    if (ack) {
        I2C1->CR1 |= I2C_CR1_ACK;  // Send ACK
    } else {
        I2C1->CR1 &= ~I2C_CR1_ACK;  // Send NACK
    }
    
    while (!(I2C1->SR1 & I2C_SR1_RXNE));  // Wait for data
    return (uint8_t)(I2C1->DR & 0xFF);
}

// High-level functions
void i2c_write(uint8_t address, uint8_t reg, uint8_t data) {
    i2c_start();
    i2c_send_address(address, 0);  // Write mode
    i2c_send_byte(reg);
    i2c_send_byte(data);
    i2c_stop();
}

uint8_t i2c_read(uint8_t address, uint8_t reg) {
    i2c_start();
    i2c_send_address(address, 0);  // Write mode
    i2c_send_byte(reg);
    
    i2c_start();  // Repeated start
    i2c_send_address(address, 1);  // Read mode
    uint8_t data = i2c_receive_byte(0);  // NACK (last byte)
    i2c_stop();
    
    return data;
}

// Example: Read from BMP280 sensor (address 0x76)
#define BMP280_ADDR  0x76
#define BMP280_ID    0xD0

uint8_t read_bmp280_id(void) {
    return i2c_read(BMP280_ADDR, BMP280_ID);
}

CHAPTER 4: INTERRUPTS AND EXCEPTION HANDLING
NVIC (Nested Vectored Interrupt Controller)
// nvic.c - Interrupt controller configuration
#include "stm32f4xx.h"

// NVIC register structure
typedef struct {
    volatile uint32_t ISER[8];      // Interrupt Set Enable (offset 0x000)
    uint32_t RESERVED0[24];
    volatile uint32_t ICER[8];      // Interrupt Clear Enable (offset 0x080)
    uint32_t RSERVED1[24];
    volatile uint32_t ISPR[8];      // Interrupt Set Pending (offset 0x100)
    uint32_t RESERVED2[24];
    volatile uint32_t ICPR[8];      // Interrupt Clear Pending (offset 0x180)
    uint32_t RESERVED3[24];
    volatile uint32_t IABR[8];      // Interrupt Active Bit (offset 0x200)
    uint32_t RESERVED4[56];
    volatile uint8_t  IP[240];      // Interrupt Priority (offset 0x300)
    uint32_t RESERVED5[644];
    volatile uint32_t STIR;         // Software Trigger Interrupt (offset 0xE00)
} NVIC_TypeDef;

#define NVIC_BASE  0xE000E100UL
#define NVIC  ((NVIC_TypeDef *) NVIC_BASE)

// Interrupt numbers (STM32F4)
#define EXTI0_IRQn        6
#define EXTI1_IRQn        7
#define EXTI2_IRQn        8
#define EXTI3_IRQn        9
#define EXTI4_IRQn        10
#define DMA1_Stream0_IRQn 11
#define DMA1_Stream1_IRQn 12
#define DMA1_Stream2_IRQn 13
#define ADC_IRQn          18
#define EXTI9_5_IRQn      23
#define TIM1_BRK_TIM9_IRQn 24
#define TIM1_UP_TIM10_IRQn 25
#define TIM1_TRG_COM_TIM11_IRQn 26
#define TIM1_CC_IRQn      27
#define TIM2_IRQn         28
#define TIM3_IRQn         29
#define TIM4_IRQn         30
#define I2C1_EV_IRQn      31
#define I2C1_ER_IRQn      32
#define SPI1_IRQn         35
#define USART1_IRQn       37
#define USART2_IRQn       38
#define USART3_IRQn       39
#define EXTI15_10_IRQn    40
#define DMA1_Stream7_IRQn 47
#define DMA2_Stream0_IRQn 56
#define DMA2_Stream1_IRQn 57
#define DMA2_Stream2_IRQn 58
#define DMA2_Stream3_IRQn 59
#define DMA2_Stream4_IRQn 60
#define DMA2_Stream5_IRQn 68
#define DMA2_Stream6_IRQn 69
#define DMA2_Stream7_IRQn 70

// Priority levels (0 = highest, 15 = lowest)
#define NVIC_PRIORITYGROUP_0  0  // 0 bits preemption, 4 bits subpriority
#define NVIC_PRIORITYGROUP_1  1  // 1 bit preemption, 3 bits subpriority
#define NVIC_PRIORITYGROUP_2  2  // 2 bits preemption, 2 bits subpriority
#define NVIC_PRIORITYGROUP_3  3  // 3 bits preemption, 1 bit subpriority
#define NVIC_PRIORITYGROUP_4  4  // 4 bits preemption, 0 bits subpriority

void nvic_set_priority(uint8_t irqn, uint8_t priority) {
    // Priority register is 8-bit, but only top 4 bits used on Cortex-M4
    NVIC->IP[irqn] = (priority << 4) & 0xF0;
}

void nvic_enable_irq(uint8_t irqn) {
    // ISER registers: each bit enables one interrupt
    // ISER[0] = IRQ 0-31, ISER[1] = IRQ 32-63, etc.
    NVIC->ISER[irqn / 32] = (1UL << (irqn % 32));
}

void nvic_disable_irq(uint8_t irqn) {
    NVIC->ICER[irqn / 32] = (1UL << (irqn % 32));
}

void nvic_clear_pending(uint8_t irqn) {
    NVIC->ICPR[irqn / 32] = (1UL << (irqn % 32));
}

void nvic_set_pending(uint8_t irqn) {
    NVIC->ISPR[irqn / 32] = (1UL << (irqn % 32));
}

int nvic_get_active(uint8_t irqn) {
    return (NVIC->IABR[irqn / 32] >> (irqn % 32)) & 1;
}

void nvic_set_priority_grouping(uint32_t group) {
    // AIRCR register (Application Interrupt and Reset Control)
    // Located at 0xE000ED0C
    volatile uint32_t *AIRCR = (volatile uint32_t *)0xE000ED0C;
    
    // Write key (0x5FA) and priority group
    *AIRCR = (0x5FA << 16) | (group << 8);
}

// Example: Configure EXTI interrupt for button
void configure_button_interrupt(void) {
    // Enable GPIOC clock
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOCEN;
    
    // Configure PC13 as input with pull-up (button on Nucleo)
    gpio_init(GPIOC, 13, GPIO_MODE_INPUT, GPIO_OTYPE_PP, GPIO_SPEED_LOW, GPIO_PUPD_UP);
    
    // Enable SYSCFG clock (for EXTI configuration)
    RCC->APB2ENR |= (1UL << 14);  // SYSCFGEN
    
    // Configure EXTI13 (PC13) to trigger on falling edge
    // EXTI->EXTICR[3] for pins 12-15
    // Select port C (0x2) for EXTI13
    SYSCFG->EXTICR[3] &= ~(0xF << 4);  // Clear bits 4-7
    SYSCFG->EXTICR[3] |= (0x2 << 4);   // Port C
    
    // Configure EXTI line 13: falling edge, interrupt mode
    EXTI->FTSR |= (1UL << 13);  // Falling trigger
    EXTI->IMR |= (1UL << 13);   // Interrupt mask (enable)
    
    // Configure NVIC
    nvic_set_priority(EXTI15_10_IRQn, 5);  // Priority 5
    nvic_enable_irq(EXTI15_10_IRQn);
}

// EXTI15_10 interrupt handler (shared for pins 10-15)
void EXTI15_10_IRQHandler(void) {
    // Check if EXTI13 triggered
    if (EXTI->PR & (1UL << 13)) {
        // Clear pending bit
        EXTI->PR = (1UL << 13);
        
        // Toggle LED
        GPIOA->ODR ^= (1UL << 5);
    }
}

SysTick Timer
// systick.c - System tick timer for RTOS
#include "stm32f4xx.h"

// SysTick register structure
typedef struct {
    volatile uint32_t CTRL;     // Control and status (offset 0x010)
    volatile uint32_t LOAD;     // Reload value (offset 0x014)
    volatile uint32_t VAL;      // Current value (offset 0x018)
    volatile uint32_t CALIB;    // Calibration (offset 0x01C)
} SysTick_TypeDef;

#define SysTick_BASE  0xE000E010UL
#define SysTick  ((SysTick_TypeDef *) SysTick_BASE)

// SysTick CTRL bits
#define SysTick_CTRL_ENABLE     (1UL << 0)
#define SysTick_CTRL_TICKINT    (1UL << 1)  // Interrupt enable
#define SysTick_CTRL_CLKSOURCE  (1UL << 2)  // Clock source (1 = processor clock)

volatile uint32_t sys_tick_counter = 0;

void systick_init(uint32_t ticks) {
    // Configure SysTick to interrupt every 'ticks' clock cycles
    SysTick->LOAD = ticks - 1;  // Reload value
    SysTick->VAL = 0;           // Clear current value
    SysTick->CTRL = SysTick_CTRL_ENABLE | 
                    SysTick_CTRL_TICKINT | 
                    SysTick_CTRL_CLKSOURCE;
    
    // Set priority (highest for RTOS)
    nvic_set_priority(15, 0);  // SysTick is IRQ 15
}

// SysTick interrupt handler
void SysTick_Handler(void) {
    sys_tick_counter++;
    
    // For RTOS: call scheduler
    // os_tick_handler();
}

uint32_t get_tick(void) {
    return sys_tick_counter;
}

void delay_ms(uint32_t ms) {
    uint32_t start = sys_tick_counter;
    while ((sys_tick_counter - start) < ms);
}

// Example: Initialize for 1 ms tick (16 MHz clock)
int main(void) {
    // Configure LED pin
    configure_gpio();
    
    // Initialize SysTick for 1 ms interrupts
    // 16 MHz / 1000 = 16000 ticks per ms
    systick_init(16000);
    
    // Enable global interrupts
    __asm__ __volatile__ ("cpsie i");
    
    while (1) {
        // Blink LED every 500 ms
        GPIOA->ODR ^= (1UL << 5);
        delay_ms(500);
    }
    
    return 0;
}

CHAPTER 5: RTOS CONCEPTS (FREERTOS)
FreeRTOS Overview
# FreeRTOS: Real-Time Operating System for microcontrollers
# Key features:
# - Preemptive multitasking
# - Priority-based scheduling
# - Real-time kernel with deterministic behavior
# - Memory management (multiple schemes)
# - Inter-task communication (queues, semaphores, mutexes)
# - Timers and software timers
# - Event groups and task notifications
# - Portable to many architectures

# FreeRTOS components:
# - Tasks: Independent threads of execution
# - Queues: Pass data between tasks
# - Semaphores: Synchronization and resource management
# - Mutexes: Mutual exclusion with priority inheritance
# - Timers: Software timers for delayed execution
# - Event Groups: Synchronize on multiple events

# FreeRTOS configuration (FreeRTOSConfig.h):
# - configUSE_PREEMPTION: Enable preemptive scheduling
# - configCPU_CLOCK_HZ: CPU clock frequency
# - configTICK_RATE_HZ: Tick rate (typically 100-1000 Hz)
# - configMAX_PRIORITIES: Maximum task priority levels
# - configTOTAL_HEAP_SIZE: Heap size for dynamic allocation
# - configUSE_MUTEXES: Enable mutex support
# - configUSE_COUNTING_SEMAPHORES: Enable counting semaphores

Hello FreeRTOS
// freertos_blinky.c - LED blink with FreeRTOS tasks
#include "FreeRTOS.h"
#include "task.h"
#include "stm32f4xx.h"

// Task handles
TaskHandle_t led_task_handle = NULL;
TaskHandle_t button_task_handle = NULL;

// LED task: toggle LED every 500 ms
void led_task(void *pvParameters) {
    // Configure LED pin
    configure_gpio();
    
    while (1) {
        // Toggle LED
        GPIOA->ODR ^= (1UL << 5);
        
        // Delay 500 ms (non-blocking)
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

// Button task: read button and print status
void button_task(void *pvParameters) {
    // Configure button pin (PC13)
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOCEN;
    gpio_init(GPIOC, 13, GPIO_MODE_INPUT, GPIO_OTYPE_PP, GPIO_SPEED_LOW, GPIO_PUPD_UP);
    
    // Configure UART for debug output
    uart_init(115200);
    
    while (1) {
        // Read button (active low)
        uint8_t button_pressed = !(GPIOC->IDR & (1UL << 13));
        
        if (button_pressed) {
            uart_send_string("Button pressed!\r\n");
        }
        
        // Check every 50 ms
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

int main(void) {
    // Initialize hardware
    SystemCoreClockUpdate();  // Update system clock variable
    
    // Create tasks
    xTaskCreate(
        led_task,           // Task function
        "LED",              // Task name
        128,                // Stack size (words)
        NULL,               // Parameters
        1,                  // Priority (1 = low)
        &led_task_handle    // Task handle
    );
    
    xTaskCreate(
        button_task,
        "Button",
        256,                // Larger stack for UART
        NULL,
        2,                  // Higher priority
        &button_task_handle
    );
    
    // Start scheduler
    vTaskStartScheduler();
    
    // Should never reach here
    while (1);
    
    return 0;
}

// SysTick handler (required by FreeRTOS)
void SysTick_Handler(void) {
    if (xTaskGetSchedulerState() != taskSCHEDULER_NOT_STARTED) {
        xPortSysTickHandler();
    }
}

CHAPTER 6: TASKS AND SCHEDULING
Task Creation and Management
// task_management.c - Advanced task operations
#include "FreeRTOS.h"
#include "task.h"
#include "stm32f4xx.h"

// Task states:
// eRunning: Task is currently executing
// eReady: Task is ready to run (waiting for CPU)
// eBlocked: Task is blocked (waiting for event/timeout)
// eSuspended: Task is suspended (manually suspended)

TaskHandle_t task1_handle = NULL;
TaskHandle_t task2_handle = NULL;
TaskHandle_t task3_handle = NULL;

// Task 1: Periodic task (every 100 ms)
void periodic_task(void *pvParameters) {
    TickType_t last_wake_time = xTaskGetTickCount();
    
    while (1) {
        // Toggle LED
        GPIOA->ODR ^= (1UL << 5);
        
        // Wait until next period (precise timing)
        vTaskDelayUntil(&last_wake_time, pdMS_TO_TICKS(100));
    }
}

// Task 2: Event-driven task
void event_task(void *pvParameters) {
    while (1) {
        // Wait for notification (from interrupt or other task)
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        // Process event
        uart_send_string("Event received!\r\n");
        
        // Do work...
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// Task 3: Continuous task (no delays)
void continuous_task(void *pvParameters) {
    uint32_t counter = 0;
    
    while (1) {
        // Do continuous work
        counter++;
        
        // Yield to other tasks (cooperative multitasking)
        taskYIELD();
    }
}

// Dynamic task creation
void create_dynamic_task(void) {
    TaskHandle_t dynamic_handle = NULL;
    
    BaseType_t status = xTaskCreate(
        continuous_task,
        "Dynamic",
        128,
        NULL,
        1,
        &dynamic_handle
    );
    
    if (status == pdPASS) {
        uart_send_string("Task created successfully\r\n");
    } else {
        uart_send_string("Failed to create task (out of memory)\r\n");
    }
}

// Task deletion
void delete_task_example(void) {
    if (task3_handle != NULL) {
        vTaskDelete(task3_handle);
        task3_handle = NULL;
        uart_send_string("Task deleted\r\n");
    }
}

// Suspend and resume
void suspend_task_example(void) {
    if (task2_handle != NULL) {
        vTaskSuspend(task2_handle);
        uart_send_string("Task suspended\r\n");
        
        vTaskDelay(pdMS_TO_TICKS(2000));
        
        vTaskResume(task2_handle);
        uart_send_string("Task resumed\r\n");
    }
}

// Get task information
void print_task_info(void) {
    char buffer[128];
    
    // Get current task handle
    TaskHandle_t current = xTaskGetCurrentTaskHandle();
    
    // Get task name
    const char *name = pcTaskGetName(current);
    snprintf(buffer, sizeof(buffer), "Current task: %s\r\n", name);
    uart_send_string(buffer);
    
    // Get task state
    eTaskState state = eTaskGetState(task1_handle);
    const char *state_str;
    switch (state) {
        case eRunning:   state_str = "Running"; break;
        case eReady:     state_str = "Ready"; break;
        case eBlocked:   state_str = "Blocked"; break;
        case eSuspended: state_str = "Suspended"; break;
        default:         state_str = "Unknown"; break;
    }
    
    snprintf(buffer, sizeof(buffer), "Task1 state: %s\r\n", state_str);
    uart_send_string(buffer);
    
    // Get stack high water mark (minimum free stack space)
    uint32_t watermark = uxTaskGetStackHighWaterMark(task1_handle);
    snprintf(buffer, sizeof(buffer), "Task1 stack watermark: %lu words\r\n", watermark);
    uart_send_string(buffer);
}

// Task priorities
void change_priority_example(void) {
    // Get current priority
    UBaseType_t old_priority = uxTaskPriorityGet(task1_handle);
    
    // Change priority
    vTaskPrioritySet(task1_handle, old_priority + 1);
    
    uart_send_string("Priority changed\r\n");
}

int main(void) {
    SystemCoreClockUpdate();
    configure_gpio();
    uart_init(115200);
    
    // Create tasks with different priorities
    xTaskCreate(periodic_task, "Periodic", 128, NULL, 2, &task1_handle);
    xTaskCreate(event_task, "Event", 256, NULL, 3, &task2_handle);
    xTaskCreate(continuous_task, "Continuous", 128, NULL, 1, &task3_handle);
    
    // Start scheduler
    vTaskStartScheduler();
    
    while (1);
    return 0;
}

Task Scheduling
# FreeRTOS scheduling algorithms:
# 1. Preemptive priority-based (default)
#    - Highest priority ready task runs
#    - Lower priority tasks preempted immediately
#
# 2. Time-sliced (round-robin)
#    - Tasks with same priority share CPU time
#    - Configured with configUSE_TIME_SLICING = 1
#
# 3. Cooperative
#    - Tasks run until they voluntarily yield
#    - Configured with configUSE_PREEMPTION = 0

# Scheduling decisions occur:
# - When a task calls vTaskDelay() or vTaskDelayUntil()
# - When a task blocks on queue/semaphore/mutex
# - When a higher priority task becomes ready
# - When an interrupt unblocks a higher priority task
# - When a task explicitly calls taskYIELD()

# Context switch:
# 1. Save current task context (registers) to stack
# 2. Load next task context from stack
# 3. Update current task pointer
# 4. Return to new task

// scheduling_demo.c - Demonstrate scheduling behavior
#include "FreeRTOS.h"
#include "task.h"

// High priority task
void high_priority_task(void *pvParameters) {
    while (1) {
        uart_send_string("H");
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

// Medium priority task
void medium_priority_task(void *pvParameters) {
    while (1) {
        uart_send_string("M");
        vTaskDelay(pdMS_TO_TICKS(200));
    }
}

// Low priority task
void low_priority_task(void *pvParameters) {
    while (1) {
        uart_send_string("L");
        vTaskDelay(pdMS_TO_TICKS(300));
    }
}

// Idle task (automatically created by FreeRTOS)
// Runs when no other tasks are ready
// Can be used for power management (WFI instruction)

// Time slicing demo (tasks with same priority)
void task_a(void *pvParameters) {
    while (1) {
        uart_send_string("A");
        // No delay - will yield to other tasks with same priority
    }
}

void task_b(void *pvParameters) {
    while (1) {
        uart_send_string("B");
    }
}

int main(void) {
    // Create tasks with different priorities
    xTaskCreate(high_priority_task, "High", 128, NULL, 3, NULL);
    xTaskCreate(medium_priority_task, "Medium", 128, NULL, 2, NULL);
    xTaskCreate(low_priority_task, "Low", 128, NULL, 1, NULL);
    
    // Or create tasks with same priority (time-sliced)
    // xTaskCreate(task_a, "A", 128, NULL, 1, NULL);
    // xTaskCreate(task_b, "B", 128, NULL, 1, NULL);
    
    vTaskStartScheduler();
    
    while (1);
    return 0;
}

CHAPTER 7: SYNCHRONIZATION PRIMITIVES
Semaphores
// semaphore_demo.c - Semaphore usage
#include "FreeRTOS.h"
#include "semphr.h"
#include "task.h"

SemaphoreHandle_t binary_semaphore = NULL;
SemaphoreHandle_t counting_semaphore = NULL;

// Binary semaphore: signaling mechanism
// Used for task-to-task or interrupt-to-task synchronization

// Producer task (interrupt handler)
void EXTI0_IRQHandler(void) {
    if (EXTI->PR & (1UL << 0)) {
        EXTI->PR = (1UL << 0);  // Clear pending
        
        // Signal consumer task
        BaseType_t higher_priority_woken = pdFALSE;
        xSemaphoreGiveFromISR(binary_semaphore, &higher_priority_woken);
        
        // Context switch if needed
        portYIELD_FROM_ISR(higher_priority_woken);
    }
}

// Consumer task
void consumer_task(void *pvParameters) {
    while (1) {
        // Wait for semaphore (block indefinitely)
        if (xSemaphoreTake(binary_semaphore, portMAX_DELAY) == pdTRUE) {
            uart_send_string("Button event processed\r\n");
            
            // Do work...
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }
}

// Counting semaphore: resource management
// Can be taken multiple times (up to max count)

#define MAX_RESOURCES 5
SemaphoreHandle_t resource_semaphore = NULL;

void resource_user_task(void *pvParameters) {
    uint32_t task_id = (uint32_t)pvParameters;
    char buffer[64];
    
    while (1) {
        // Try to acquire resource
        if (xSemaphoreTake(resource_semaphore, pdMS_TO_TICKS(1000)) == pdTRUE) {
            snprintf(buffer, sizeof(buffer), "Task %lu acquired resource\r\n", task_id);
            uart_send_string(buffer);
            
            // Use resource
            vTaskDelay(pdMS_TO_TICKS(500));
            
            // Release resource
            xSemaphoreGive(resource_semaphore);
            
            snprintf(buffer, sizeof(buffer), "Task %lu released resource\r\n", task_id);
            uart_send_string(buffer);
        } else {
            snprintf(buffer, sizeof(buffer), "Task %lu timeout waiting for resource\r\n", task_id);
            uart_send_string(buffer);
        }
        
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

int main(void) {
    // Create binary semaphore (initially empty)
    binary_semaphore = xSemaphoreCreateBinary();
    
    // Create counting semaphore (initial count = MAX_RESOURCES)
    resource_semaphore = xSemaphoreCreateCounting(MAX_RESOURCES, MAX_RESOURCES);
    
    // Create consumer task
    xTaskCreate(consumer_task, "Consumer", 256, NULL, 2, NULL);
    
    // Create resource user tasks
    for (uint32_t i = 0; i < 10; i++) {
        xTaskCreate(resource_user_task, "Resource", 256, (void *)i, 1, NULL);
    }
    
    vTaskStartScheduler();
    
    while (1);
    return 0;
}

Mutexes
// mutex_demo.c - Mutex for mutual exclusion
#include "FreeRTOS.h"
#include "semphr.h"
#include "task.h"

SemaphoreHandle_t uart_mutex = NULL;

// Shared resource: UART
void print_task(void *pvParameters) {
    const char *task_name = (const char *)pvParameters;
    char buffer[128];
    
    while (1) {
        // Acquire mutex
        if (xSemaphoreTake(uart_mutex, portMAX_DELAY) == pdTRUE) {
            // Critical section: exclusive access to UART
            snprintf(buffer, sizeof(buffer), "[%s] Using UART\r\n", task_name);
            uart_send_string(buffer);
            
            // Simulate work
            vTaskDelay(pdMS_TO_TICKS(100));
            
            snprintf(buffer, sizeof(buffer), "[%s] Done with UART\r\n", task_name);
            uart_send_string(buffer);
            
            // Release mutex
            xSemaphoreGive(uart_mutex);
        }
        
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

// Priority inheritance demo
// Mutex prevents priority inversion:
// - Low priority task holds mutex
// - High priority task wants mutex (blocks)
// - Medium priority task preempts low priority
// - With priority inheritance: low priority temporarily gets high priority

SemaphoreHandle_t shared_mutex = NULL;

void low_priority_task(void *pvParameters) {
    while (1) {
        if (xSemaphoreTake(shared_mutex, portMAX_DELAY) == pdTRUE) {
            uart_send_string("Low: acquired mutex\r\n");
            
            // Hold mutex for a while
            vTaskDelay(pdMS_TO_TICKS(1000));
            
            xSemaphoreGive(shared_mutex);
            uart_send_string("Low: released mutex\r\n");
        }
        
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

void medium_priority_task(void *pvParameters) {
    while (1) {
        uart_send_string("Medium: running\r\n");
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void high_priority_task(void *pvParameters) {
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(500));
        
        uart_send_string("High: waiting for mutex\r\n");
        
        if (xSemaphoreTake(shared_mutex, portMAX_DELAY) == pdTRUE) {
            uart_send_string("High: acquired mutex\r\n");
            vTaskDelay(pdMS_TO_TICKS(100));
            xSemaphoreGive(shared_mutex);
            uart_send_string("High: released mutex\r\n");
        }
    }
}

int main(void) {
    // Create mutex (recursive mutex allows same task to take multiple times)
    uart_mutex = xSemaphoreCreateMutex();
    shared_mutex = xSemaphoreCreateMutex();
    // SemaphoreHandle_t recursive_mutex = xSemaphoreCreateRecursiveMutex();
    
    // Create tasks
    xTaskCreate(print_task, "Task1", 256, "Task1", 1, NULL);
    xTaskCreate(print_task, "Task2", 256, "Task2", 1, NULL);
    
    // Priority inheritance demo
    xTaskCreate(low_priority_task, "Low", 256, NULL, 1, NULL);
    xTaskCreate(medium_priority_task, "Medium", 256, NULL, 2, NULL);
    xTaskCreate(high_priority_task, "High", 256, NULL, 3, NULL);
    
    vTaskStartScheduler();
    
    while (1);
    return 0;
}

CHAPTER 8: INTER-TASK COMMUNICATION
Queues
// queue_demo.c - Queue for inter-task communication
#include "FreeRTOS.h"
#include "queue.h"
#include "task.h"

// Queue for sensor data
typedef struct {
    uint32_t timestamp;
    float temperature;
    float humidity;
    uint8_t sensor_id;
} sensor_data_t;

QueueHandle_t sensor_queue = NULL;

// Producer task: read sensors and send to queue
void sensor_task(void *pvParameters) {
    sensor_data_t data;
    uint8_t sensor_id = 0;
    
    while (1) {
        // Read sensor (simulated)
        data.timestamp = xTaskGetTickCount();
        data.temperature = 20.0f + (rand() % 100) / 10.0f;
        data.humidity = 50.0f + (rand() % 300) / 10.0f;
        data.sensor_id = sensor_id++;
        
        // Send to queue (wait up to 100 ms if queue full)
        if (xQueueSend(sensor_queue, &data, pdMS_TO_TICKS(100)) == pdTRUE) {
            uart_send_string("Sensor data sent\r\n");
        } else {
            uart_send_string("Queue full!\r\n");
        }
        
        // Read every 500 ms
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

// Consumer task: receive and process sensor data
void processing_task(void *pvParameters) {
    sensor_data_t data;
    
    while (1) {
        // Receive from queue (block indefinitely)
        if (xQueueReceive(sensor_queue, &data, portMAX_DELAY) == pdTRUE) {
            char buffer[128];
            snprintf(buffer, sizeof(buffer), 
                     "Received: ID=%u, T=%.1f°C, H=%.1f%%, T=%lu\r\n",
                     data.sensor_id, data.temperature, data.humidity, data.timestamp);
            uart_send_string(buffer);
            
            // Process data...
        }
    }
}

// Queue sets: wait on multiple queues
QueueHandle_t queue1 = NULL;
QueueHandle_t queue2 = NULL;
QueueSetHandle_t queue_set = NULL;

void producer1_task(void *pvParameters) {
    uint32_t value = 0;
    while (1) {
        xQueueSend(queue1, &value, portMAX_DELAY);
        value++;
        vTaskDelay(pdMS_TO_TICKS(300));
    }
}

void producer2_task(void *pvParameters) {
    uint32_t value = 1000;
    while (1) {
        xQueueSend(queue2, &value, portMAX_DELAY);
        value++;
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void consumer_task(void *pvParameters) {
    while (1) {
        // Wait for any queue in the set
        QueueSetMemberHandle_t active_queue = xQueueSelectFromSet(queue_set, portMAX_DELAY);
        
        uint32_t value;
        if (active_queue == queue1) {
            xQueueReceive(queue1, &value, 0);
            snprintf(buffer, sizeof(buffer), "Queue1: %lu\r\n", value);
            uart_send_string(buffer);
        } else if (active_queue == queue2) {
            xQueueReceive(queue2, &value, 0);
            snprintf(buffer, sizeof(buffer), "Queue2: %lu\r\n", value);
            uart_send_string(buffer);
        }
    }
}

int main(void) {
    // Create queue (holds 10 sensor_data_t items)
    sensor_queue = xQueueCreate(10, sizeof(sensor_data_t));
    
    // Create tasks
    xTaskCreate(sensor_task, "Sensor", 256, NULL, 2, NULL);
    xTaskCreate(processing_task, "Process", 512, NULL, 1, NULL);
    
    // Queue set demo
    queue1 = xQueueCreate(5, sizeof(uint32_t));
    queue2 = xQueueCreate(5, sizeof(uint32_t));
    queue_set = xQueueCreateSet(10);  // Total items in all queues
    
    xQueueAddToSet(queue1, queue_set);
    xQueueAddToSet(queue2, queue_set);
    
    xTaskCreate(producer1_task, "Prod1", 128, NULL, 1, NULL);
    xTaskCreate(producer2_task, "Prod2", 128, NULL, 1, NULL);
    xTaskCreate(consumer_task, "Cons", 256, NULL, 2, NULL);
    
    vTaskStartScheduler();
    
    while (1);
    return 0;
}

Task Notifications
// notification_demo.c - Lightweight alternative to binary semaphores
#include "FreeRTOS.h"
#include "task.h"

TaskHandle_t worker_task_handle = NULL;

// Worker task: waits for notifications
void worker_task(void *pvParameters) {
    while (1) {
        // Wait for notification (like binary semaphore)
        uint32_t notification_value = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        if (notification_value > 0) {
            uart_send_string("Worker: notification received\r\n");
            
            // Process work...
            vTaskDelay(pdMS_TO_TICKS(100));
        }
    }
}

// ISR: send notification to task
void EXTI0_IRQHandler(void) {
    if (EXTI->PR & (1UL << 0)) {
        EXTI->PR = (1UL << 0);
        
        // Notify task (from ISR)
        BaseType_t higher_priority_woken = pdFALSE;
        vTaskNotifyGiveFromISR(worker_task_handle, &higher_priority_woken);
        
        portYIELD_FROM_ISR(higher_priority_woken);
    }
}

// Task: send notification with value
void controller_task(void *pvParameters) {
    uint32_t command = 0;
    
    while (1) {
        // Send notification with value
        xTaskNotify(worker_task_handle, command, eSetValueWithOverwrite);
        
        command++;
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

// Advanced notification: wait for specific bits
void advanced_worker_task(void *pvParameters) {
    while (1) {
        // Wait for bits 0 and 1 to be set
        uint32_t notified_value;
        xTaskNotifyWait(
            0x00,              // Don't clear bits on entry
            0xFFFFFFFF,        // Clear all bits on exit
            &notified_value,   // Receive notified value
            portMAX_DELAY
        );
        
        if (notified_value & 0x01) {
            uart_send_string("Bit 0 set\r\n");
        }
        if (notified_value & 0x02) {
            uart_send_string("Bit 1 set\r\n");
        }
    }
}

int main(void) {
    xTaskCreate(worker_task, "Worker", 256, NULL, 2, &worker_task_handle);
    xTaskCreate(controller_task, "Controller", 256, NULL, 1, NULL);
    
    vTaskStartScheduler();
    
    while (1);
    return 0;
}

CHAPTER 9: DEVICE DRIVERS
ADC Driver
// adc.c - Analog-to-Digital Converter driver
#include "stm32f4xx.h"

// ADC1 register structure
typedef struct {
    volatile uint32_t SR;      // Status register
    volatile uint32_t CR1;     // Control register 1
    volatile uint32_t CR2;     // Control register 2
    volatile uint32_t SMPR1;   // Sample time register 1
    volatile uint32_t SMPR2;   // Sample time register 2
    volatile uint32_t JOFR1;   // Injected channel data offset 1
    volatile uint32_t JOFR2;   // Injected channel data offset 2
    volatile uint32_t JOFR3;   // Injected channel data offset 3
    volatile uint32_t JOFR4;   // Injected channel data offset 4
    volatile uint32_t HTR;     // Watchdog higher threshold
    volatile uint32_t LTR;     // Watchdog lower threshold
    volatile uint32_t SQR1;    // Regular sequence register 1
    volatile uint32_t SQR2;    // Regular sequence register 2
    volatile uint32_t SQR3;    // Regular sequence register 3
    volatile uint32_t JSQR;    // Injected sequence register
    volatile uint32_t JDR1;    // Injected data register 1
    volatile uint32_t JDR2;    // Injected data register 2
    volatile uint32_t JDR3;    // Injected data register 3
    volatile uint32_t JDR4;    // Injected data register 4
    volatile uint32_t DR;      // Data register
} ADC_TypeDef;

#define ADC1_BASE  0x40012000UL
#define ADC1  ((ADC_TypeDef *) ADC1_BASE)

// Common ADC registers
typedef struct {
    volatile uint32_t CSR;     // Common status register
    volatile uint32_t CCR;     // Common control register
    volatile uint32_t CDR;     // Common regular data register
} ADC_Common_TypeDef;

#define ADC_COMMON_BASE  0x40012300UL
#define ADC_COMMON  ((ADC_Common_TypeDef *) ADC_COMMON_BASE)

// Status register bits
#define ADC_SR_EOC   (1UL << 1)  // End of conversion
#define ADC_SR_STRT  (1UL << 4)  // Start flag

// Control register 2 bits
#define ADC_CR2_ADON   (1UL << 0)   // ADC on/off
#define ADC_CR2_CONT   (1UL << 1)   // Continuous conversion
#define ADC_CR2_SWSTART (1UL << 30) // Start conversion

void adc_init(void) {
    // Enable GPIOA and ADC1 clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB2ENR |= (1UL << 8);  // ADC1EN (bit 8)
    
    // Configure PA0 as analog input (ADC1_IN0)
    gpio_init(GPIOA, 0, GPIO_MODE_ANALOG, GPIO_OTYPE_PP, GPIO_SPEED_LOW, GPIO_PUPD_NONE);
    
    // Configure ADC common settings
    ADC_COMMON->CCR = 0;  // Independent mode, async clock
    
    // Configure ADC1
    ADC1->CR1 = 0;  // 12-bit resolution, single conversion
    ADC1->CR2 = 0;  // Right-aligned, single conversion
    ADC1->SMPR1 = 0;
    ADC1->SMPR2 = (7UL << 0);  // Channel 0: 480 cycles sample time
    
    // Configure regular sequence: 1 conversion (channel 0)
    ADC1->SQR1 = 0;  // 1 conversion
    ADC1->SQR3 = 0;  // Channel 0 in first position
    
    // Enable ADC
    ADC1->CR2 |= ADC_CR2_ADON;
    
    // Calibration (recommended after power-on)
    ADC1->CR2 |= ADC_CR2_ADON;  // Wait 2 ADC clock cycles
}

uint16_t adc_read(void) {
    // Start conversion
    ADC1->CR2 |= ADC_CR2_SWSTART;
    
    // Wait for conversion to complete
    while (!(ADC1->SR & ADC_SR_EOC));
    
    // Read result (12-bit, right-aligned)
    return (uint16_t)(ADC1->DR & 0x0FFF);
}

float adc_to_voltage(uint16_t adc_value, float vref) {
    // Convert ADC value to voltage
    // V = (ADC_value / 4096) * Vref
    return ((float)adc_value / 4096.0f) * vref;
}

// Example usage
int main(void) {
    adc_init();
    uart_init(115200);
    
    while (1) {
        uint16_t adc_value = adc_read();
        float voltage = adc_to_voltage(adc_value, 3.3f);
        
        char buffer[64];
        snprintf(buffer, sizeof(buffer), "ADC: %u (%.2f V)\r\n", adc_value, voltage);
        uart_send_string(buffer);
        
        vTaskDelay(pdMS_TO_TICKS(500));
    }
    
    return 0;
}

PWM Driver
// pwm.c - Pulse Width Modulation driver
#include "stm32f4xx.h"

// TIM2 register structure
typedef struct {
    volatile uint32_t CR1;     // Control register 1
    volatile uint32_t CR2;     // Control register 2
    volatile uint32_t SMCR;    // Slave mode control
    volatile uint32_t DIER;    // DMA/interrupt enable
    volatile uint32_t SR;      // Status register
    volatile uint32_t EGR;     // Event generation
    volatile uint32_t CCMR1;   // Capture/compare mode 1
    volatile uint32_t CCMR2;   // Capture/compare mode 2
    volatile uint32_t CCER;    // Capture/compare enable
    volatile uint32_t CNT;     // Counter
    volatile uint32_t PSC;     // Prescaler
    volatile uint32_t ARR;     // Auto-reload
    volatile uint32_t RCR;     // Repetition counter
    volatile uint32_t CCR1;    // Capture/compare 1
    volatile uint32_t CCR2;    // Capture/compare 2
    volatile uint32_t CCR3;    // Capture/compare 3
    volatile uint32_t CCR4;    // Capture/compare 4
    volatile uint32_t BDTR;    // Break and dead-time
    volatile uint32_t DCR;     // DMA control
    volatile uint32_t DMAR;    // DMA address for full transfer
} TIM_TypeDef;

#define TIM2_BASE  0x40000000UL
#define TIM2  ((TIM_TypeDef *) TIM2_BASE)

// Control register 1 bits
#define TIM_CR1_CEN  (1UL << 0)   // Counter enable
#define TIM_CR1_ARPE (1UL << 7)   // Auto-reload preload enable

// Capture/compare mode register bits
#define TIM_CCMR1_OC1M   (7UL << 4)   // Output compare 1 mode
#define TIM_CCMR1_OC1PE  (1UL << 3)   // Output compare 1 preload enable

// Capture/compare enable register bits
#define TIM_CCER_CC1E  (1UL << 0)   // Capture/compare 1 output enable

// PWM modes
#define PWM_MODE1  0x06  // PWM mode 1: active when CNT < CCR
#define PWM_MODE2  0x07  // PWM mode 2: active when CNT > CCR

void pwm_init(uint32_t frequency_hz) {
    // Enable GPIOA and TIM2 clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB1ENR |= (1UL << 0);  // TIM2EN (bit 0)
    
    // Configure PA5 as alternate function AF1 (TIM2_CH1)
    gpio_init(GPIOA, 5, GPIO_MODE_AF, GPIO_OTYPE_PP, GPIO_SPEED_HIGH, GPIO_PUPD_NONE);
    gpio_set_af(GPIOA, 5, 1);  // AF1 = TIM2
    
    // Configure timer
    // PWM frequency = TIM_CLK / (PSC + 1) / (ARR + 1)
    // For 16 MHz TIM2 clock, 1 kHz PWM:
    // PSC = 15, ARR = 999 → 16M / 16 / 1000 = 1 kHz
    
    uint32_t tim_clk = 16000000;  // 16 MHz
    uint32_t psc = (tim_clk / (frequency_hz * 1000)) - 1;
    uint32_t arr = 999;  // 1000 steps (0-999)
    
    TIM2->PSC = psc;
    TIM2->ARR = arr;
    
    // Configure channel 1 as PWM
    TIM2->CCMR1 &= ~TIM_CCMR1_OC1M;  // Clear mode bits
    TIM2->CCMR1 |= (PWM_MODE1 << 4);  // PWM mode 1
    TIM2->CCMR1 |= TIM_CCMR1_OC1PE;   // Preload enable
    
    // Enable channel 1 output
    TIM2->CCER |= TIM_CCER_CC1E;
    
    // Set initial duty cycle (50%)
    TIM2->CCR1 = arr / 2;
    
    // Enable auto-reload preload
    TIM2->CR1 |= TIM_CR1_ARPE;
    
    // Start timer
    TIM2->CR1 |= TIM_CR1_CEN;
}

void pwm_set_duty(uint16_t duty_percent) {
    // duty_percent: 0-100
    if (duty_percent > 100) duty_percent = 100;
    
    uint32_t arr = TIM2->ARR;
    uint32_t ccr = (arr * duty_percent) / 100;
    
    TIM2->CCR1 = ccr;
}

void pwm_set_duty_raw(uint16_t value) {
    // value: 0-ARR
    TIM2->CCR1 = value;
}

// Example: fade LED
int main(void) {
    pwm_init(1000);  // 1 kHz PWM
    
    while (1) {
        // Fade in
        for (uint16_t duty = 0; duty <= 100; duty++) {
            pwm_set_duty(duty);
            vTaskDelay(pdMS_TO_TICKS(10));
        }
        
        // Fade out
        for (uint16_t duty = 100; duty > 0; duty--) {
            pwm_set_duty(duty);
            vTaskDelay(pdMS_TO_TICKS(10));
        }
    }
    
    return 0;
}

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
DMA (Direct Memory Access)
// dma.c - DMA configuration for efficient data transfer
#include "stm32f4xx.h"

// DMA2 register structure
typedef struct {
    volatile uint32_t LISR;    // Low interrupt status
    volatile uint32_t HISR;    // High interrupt status
    volatile uint32_t LIFCR;   // Low interrupt flag clear
    volatile uint32_t HIFCR;   // High interrupt flag clear
} DMA_TypeDef;

#define DMA2_BASE  0x40020400UL
#define DMA2  ((DMA_TypeDef *) DMA2_BASE)

// DMA stream register structure
typedef struct {
    volatile uint32_t CR;      // Configuration
    volatile uint32_t NDTR;    // Number of data
    volatile uint32_t PAR;     // Peripheral address
    volatile uint32_t M0AR;    // Memory 0 address
    volatile uint32_t M1AR;    // Memory 1 address
    volatile uint32_t FCR;     // FIFO control
} DMA_Stream_TypeDef;

#define DMA2_Stream0_BASE  (DMA2_BASE + 0x10)
#define DMA2_Stream0  ((DMA_Stream_TypeDef *) DMA2_Stream0_BASE)

// DMA stream CR bits
#define DMA_CR_EN     (1UL << 0)    // Stream enable
#define DMA_CR_TCIE   (1UL << 4)    // Transfer complete interrupt enable
#define DMA_CR_CIRC   (1UL << 8)    // Circular mode
#define DMA_CR_DIR    (3UL << 6)    // Direction
#define DMA_CR_MINC   (1UL << 10)   // Memory increment mode
#define DMA_CR_PSIZE  (3UL << 11)   // Peripheral size
#define DMA_CR_MSIZE  (3UL << 13)   // Memory size
#define DMA_CR_PL     (3UL << 16)   // Priority level

// DMA directions
#define DMA_DIR_PERIPH_TO_MEM  (0UL << 6)
#define DMA_DIR_MEM_TO_PERIPH  (1UL << 6)
#define DMA_DIR_MEM_TO_MEM     (2UL << 6)

// DMA data sizes
#define DMA_SIZE_BYTE      (0UL << 0)
#define DMA_SIZE_HALFWORD  (1UL << 0)
#define DMA_SIZE_WORD      (2UL << 0)

void dma_init_adc(void) {
    // Enable DMA2 clock
    RCC->AHB1ENR |= (1UL << 22);  // DMA2EN (bit 22)
    
    // Configure DMA2 Stream0 for ADC1
    DMA2_Stream0->CR = 0;  // Disable stream
    
    // Wait until stream is disabled
    while (DMA2_Stream0->CR & DMA_CR_EN);
    
    // Configure stream
    DMA2_Stream0->CR = DMA_DIR_PERIPH_TO_MEM |  // Peripheral to memory
                       (DMA_SIZE_HALFWORD << 11) |  // Peripheral: half-word
                       (DMA_SIZE_HALFWORD << 13) |  // Memory: half-word
                       DMA_CR_MINC |              // Memory increment
                       DMA_CR_CIRC |              // Circular mode
                       DMA_CR_TCIE |              // Transfer complete interrupt
                       (0UL << 16);               // Priority: low
    
    // Peripheral address (ADC1 data register)
    DMA2_Stream0->PAR = (uint32_t)&ADC1->DR;
    
    // Memory address (destination buffer)
    extern uint16_t adc_buffer[100];
    DMA2_Stream0->M0AR = (uint32_t)adc_buffer;
    
    // Number of data items
    DMA2_Stream0->NDTR = 100;
    
    // Channel selection (ADC1 = channel 0)
    DMA2_Stream0->CR |= (0UL << 25);  // Channel 0
    
    // Enable ADC DMA request
    ADC1->CR2 |= (1UL << 8);  // DMA enable
    
    // Enable stream
    DMA2_Stream0->CR |= DMA_CR_EN;
}

// DMA transfer complete interrupt
void DMA2_Stream0_IRQHandler(void) {
    // Check transfer complete flag
    if (DMA2->LISR & (1UL << 5)) {  // TCIF0 (bit 5)
        // Clear flag
        DMA2->LIFCR = (1UL << 5);
        
        // Process ADC buffer
        extern uint16_t adc_buffer[100];
        // ... process data ...
    }
}

Low Power Modes
// low_power.c - Power management
#include "stm32f4xx.h"

// Enter sleep mode (CPU stopped, peripherals running)
void enter_sleep_mode(void) {
    // Clear SLEEPDEEP bit in Cortex-M4 System Control Register
    SCB->SCR &= ~(1UL << 2);
    
    // Execute WFI (Wait For Interrupt) instruction
    __asm__ __volatile__ ("wfi");
}

// Enter stop mode (CPU and most peripherals stopped)
void enter_stop_mode(void) {
    // Configure PWR register
    PWR->CR |= (1UL << 0);  // Low-power regulator
    
    // Set SLEEPDEEP bit
    SCB->SCR |= (1UL << 2);
    
    // Enter STOP mode
    __asm__ __volatile__ ("wfi");
    
    // Clear SLEEPDEEP bit after wakeup
    SCB->SCR &= ~(1UL << 2);
}

// Enter standby mode (lowest power, only RTC and wakeup pins active)
void enter_standby_mode(void) {
    // Clear wakeup flag
    PWR->CR |= (1UL << 2);
    
    // Enable standby mode
    PWR->CR |= (1UL << 1);
    
    // Set SLEEPDEEP bit
    SCB->SCR |= (1UL << 2);
    
    // Enter STANDBY mode
    __asm__ __volatile__ ("wfi");
    
    // System resets on wakeup from standby
}

// Wakeup sources:
// - External interrupt (EXTI)
// - RTC alarm
// - USART RX
// - USB OTG FS

Debugging and Profiling
# Debugging tools:
# - GDB + OpenOCD: Command-line debugging
# - STM32CubeIDE: Integrated IDE with debugger
# - Segger J-Link: High-performance debug probe
# - Logic analyzer: Protocol analysis (UART, SPI, I2C)
# - Oscilloscope: Signal visualization

# Debugging techniques:
# - Breakpoints: Halt execution at specific lines
# - Watchpoints: Halt when variable changes
# - Step/Step over/Step out: Execute line by line
# - Registers view: Inspect CPU registers
# - Memory view: Inspect RAM/Flash contents
# - Peripheral view: Inspect peripheral registers
# - Call stack: View function call hierarchy
# - Disassembly: View generated assembly code

# Profiling techniques:
# - Cycle counter (DWT_CYCCNT): Measure execution time
# - GPIO toggling: Measure timing with oscilloscope
# - ITM (Instrumentation Trace Macrocell): Trace output
# - ETM (Embedded Trace Macrocell): Full instruction trace

// profiling.c - Performance measurement
#include "stm32f4xx.h"

// DWT (Data Watchpoint and Trace) registers
#define DWT_CTRL   (*(volatile uint32_t *)0xE0001000)
#define DWT_CYCCNT (*(volatile uint32_t *)0xE0001004)

void enable_cycle_counter(void) {
    // Enable TRC bit in DEMCR (Debug Exception and Monitor Control Register)
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    
    // Reset cycle counter
    DWT_CYCCNT = 0;
    
    // Enable cycle counter
    DWT_CTRL |= 1;
}

uint32_t get_cycles(void) {
    return DWT_CYCCNT;
}

float cycles_to_us(uint32_t cycles, uint32_t cpu_freq_hz) {
    return (float)cycles / (cpu_freq_hz / 1000000.0f);
}

// Example: measure function execution time
void measure_function(void) {
    enable_cycle_counter();
    
    uint32_t start = get_cycles();
    
    // Function to measure
    uart_send_string("Hello, World!\r\n");
    
    uint32_t end = get_cycles();
    uint32_t cycles = end - start;
    
    char buffer[64];
    snprintf(buffer, sizeof(buffer), "Execution time: %lu cycles (%.2f us)\r\n",
             cycles, cycles_to_us(cycles, 16000000));
    uart_send_string(buffer);
}

Recommended Reading
# - "Making Embedded Systems" by Elecia White
# - "The Art of Designing Embedded Systems" by Jack Ganssle
# - "Programming Interactivity" by Joshua Noble
# - "Mastering STM32" by Carmine Noviello (free online)
# - "The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors" by Joseph Yiu
# - FreeRTOS documentation: https://www.freertos.org/
# - ARM Cortex-M4 technical reference manual
# - STM32F4 reference manual

# Online Resources
# - STM32CubeMX: https://www.st.com/en/development-tools/stm32cubemx.html
# - FreeRTOS: https://www.freertos.org/
# - ARM Developer: https://developer.arm.com/
# - Embedded Artistry: https://embeddedartistry.com/
# - Interrupt (Memfault blog): https://interrupt.memfault.com/
# - EEVblog: https://www.eevblog.com/

# End of Embedded Systems & RTOS Reference