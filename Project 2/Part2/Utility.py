def getEncodingOption():
    print("Available Encoding Options:")
    print("1. No PC")
    print("2. Predictive encoding with Predictor A")
    print("3. Predictive encoding with Predictor B")
    print("4. Predictive encoding with Predictor C")
    print("5. Predictive encoding with a1 * A + a2 * B + a3 * C")
    return (raw_input("Select an option :"))

def getPixelRegion():
    return input("Enter the origin of the 10x10 pixel region: ")
