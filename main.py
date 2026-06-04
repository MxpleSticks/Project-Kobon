import sys
import subprocess
from Solver.state import create_random_state

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
            arrangement = create_random_state(k)
            goal_input = parts[3].lower()
            if(goal_input not in ("ma","mi")):
                print("Error: Last parameter must be 'ma' or 'mi'.")
                return
            goal_text = "MAXIMIZE" if goal_input == "ma" else "MINIMIZE"
            print(f"\nConfiguration complete. Running {goal_text} solver...")
            # run_annealing(k, iters, restarts, goal_text)

        
        elif(choice == 2):
            print("Usage: <k> <reset_every> <ma/mi> <target gap>")
            print("reset_every: how many iterations before restarting with a new random arrangement")
            
            parts = input("Enter parameters: ").split()
            
            if(len(parts) != 4):
                print("Error: Please provide all 4 parameters.")
                return
            
            k, reset_every = int(parts[0]), int(parts[1])      
            arrangement = create_random_state(k)     
            goal_input = parts[2].lower()
            if(goal_input not in ("ma","mi")):
                print("Error: Last parameter must be 'ma' or 'mi'.")
                return
            goal_text = "MAXIMIZE" if goal_input == "ma" else "MINIMIZE"
            target_gap = int(parts[3])
            print(f"\nRunning {goal_text} solver, resetting every {reset_every} iterations until within {target_gap} of ceiling...")
            # run_annealing_until(k, reset_every, goal_text, target_gap)

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