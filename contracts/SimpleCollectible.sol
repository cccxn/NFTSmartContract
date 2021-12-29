// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0 ;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol" ;
//import "./test/ERC721.sol" ;

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter ;
    mapping (uint256 => string) private _tokenURIs ;


    constructor () public ERC721 ("Doggie", "DOG"){
        tokenCounter = 0 ;
    }
    // Added my CCCXN based on https://forum.openzeppelin.com/t/function-settokenuri-in-erc721-is-gone-with-pragma-0-8-0/5978/14
    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal virtual {
        require(_exists(tokenId), "ERC721Metadata: URI set of nonexistent token");
        _tokenURIs[tokenId] = _tokenURI;
    }

    function createCollectible(string memory tokenURI) public returns (uint256){
        uint256 newTokenId = tokenCounter ;
        _safeMint(msg.sender, newTokenId) ;
        _setTokenURI(newTokenId, tokenURI) ;
        tokenCounter = tokenCounter + 1;
        return newTokenId ;
    }
}