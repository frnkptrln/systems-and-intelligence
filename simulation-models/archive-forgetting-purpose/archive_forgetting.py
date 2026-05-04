"""Scaffold simulation: selective forgetting vs identity persistence."""

import random


def run(steps: int = 100, retain_rate: float = 0.9, ritual_erase_interval: int = 20):
    memory = []
    ip_proxy = 0.5
    for t in range(steps):
        event = random.uniform(-1, 1)
        memory.append(event)
        memory = [m for m in memory if random.random() < retain_rate]
        if ritual_erase_interval and t % ritual_erase_interval == 0 and t > 0:
            memory = memory[len(memory)//4:]
        volatility = sum(abs(m) for m in memory[-10:]) / max(1, min(10, len(memory)))
        ip_proxy = max(0.0, min(1.0, 1.0 / (1.0 + volatility)))
    return {"memory_size": len(memory), "ip_proxy": ip_proxy}


if __name__ == "__main__":
    print(run())
