"""Example: plot dark energy delta_norm(z)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import plot_delta
plt = plot_delta(-0.75, -0.87)
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "delta_plot.png"))
print("saved delta_plot.png")
