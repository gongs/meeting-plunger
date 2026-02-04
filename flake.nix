{
  description = "Meeting Plunger - A monorepo with Python FastAPI backend and Golang CLI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Python with FastAPI and common dependencies
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          fastapi
          uvicorn
          pydantic
          httpx
          pytest
          pytest-asyncio
          python-multipart
          python-dotenv
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python environment
            pythonEnv
            
            # Golang
            go
            
            # Development tools
            git
            
            # Optional but useful
            curl
            jq
          ];

          shellHook = ''
            echo "🚀 Meeting Plunger Development Environment"
            echo ""
            echo "Available tools:"
            echo "  Python: $(python --version)"
            echo "  Go:     $(go version)"
            echo ""
            echo "Project structure:"
            echo "  backend/  - Python FastAPI backend"
            echo "  client/   - Golang CLI and local HTTP service"
            echo ""
            echo "Get started:"
            echo "  cd backend && uvicorn main:app --reload"
            echo "  cd client && go run ."
          '';
        };
      }
    );
}
