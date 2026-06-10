import sys
import subprocess
from Solver.state import createRandomState
from Solver.annealing import runAnnealingUntil, runAnnealing

def main():
    print("=============================\n∥       Project Kobon       ∥\n=============================")
    print("1. Run solver")
    print("2. Run until target")
    print("3. Open viewer")
    

    try:
        choice = int(input("Select an option (1-3): "))

        if(choice not in (1,2,3)):
            print("Error: Invalid input format.")
            return

        if(choice == 1):
            print("Usage: <k> <iterations> <restarts> <ma/mi>")
            
            parts = input("Enter parameters: ").split()
            
            if(len(parts) != 4):
                print("Error: Please provide all 4 parameters.")
                return
            
            k, iters, restarts = int(parts[0]), int(parts[1]), int(parts[2])
            arrangement = createRandomState(k)
            goalInput = parts[3].lower()
            if(goalInput not in ("ma","mi")):
                print("Error: Last parameter must be 'ma' or 'mi'.")
                return
            goalText = "MAXIMIZE" if goalInput == "ma" else "MINIMIZE"
            print(f"\nConfiguration complete. Running {goalText} solver...")
            
            runAnnealing(k, iters, restarts, goalText)

        
        elif(choice == 2):
            print("Usage: <k> <reset every> <ma/mi> <target gap>")
            print("reset every: how many iterations before restarting with a new random arrangement")
            
            parts = input("Enter parameters: ").split()
            
            if(len(parts) != 4):
                print("Error: Please provide all 4 parameters.")
                return
            
            k, resetEvery = int(parts[0]), int(parts[1])      
            arrangement = createRandomState(k)     
            goalInput = parts[2].lower()
            if(goalInput not in ("ma","mi")):
                print("Error: Last parameter must be 'ma' or 'mi'.")
                return
            goalText = "MAXIMIZE" if goalInput == "ma" else "MINIMIZE"
            targetGap = int(parts[3])
            print(f"\nRunning {goalText} solver, resetting every {resetEvery} iterations until within {targetGap} of ceiling...")
            
            runAnnealingUntil(k, resetEvery, goalText, targetGap)

        elif(choice == 3):
            print("Opening viewer.py shortly...")
            
            subprocess.run([sys.executable, "Viewer/viewer.py"])
    
    
    except ValueError:
        print("Error: Invalid input format.")

    except KeyboardInterrupt:
        print("\nProcess stopped.")
        sys.exit()



if __name__ == "__main__":
    main()